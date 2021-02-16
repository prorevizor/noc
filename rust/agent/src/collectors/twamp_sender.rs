// ---------------------------------------------------------------------
// TWAMP Sender
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------
use crate::collectors::base::{Collectable, Collector, Status};
use crate::proto::connection::Connection;
use crate::proto::frame::{FrameReader, FrameWriter};
use crate::proto::pktmodel::{get_packet_model, PacketModel};
use crate::proto::tos::dscp_to_tos;
use crate::proto::twamp::{
    AcceptSession, RequestTWSession, ServerGreeting, ServerStart, SetupResponse, StartAck,
    StartSessions, StopSessions, TestRequest, TestResponse, UTCDateTime, ACCEPT_OK, MODE_REFUSED,
    MODE_UNAUTHENTICATED,
};
use crate::timing::Timing;
use crate::zk::Configurable;
use async_trait::async_trait;
use bytes::{Bytes, BytesMut};
use chrono::Utc;
use serde::Deserialize;
use std::collections::HashMap;
use std::error::Error;
use std::net::SocketAddr;
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::net::{TcpStream, UdpSocket};

#[derive(Deserialize, Debug)]
pub struct TWAMPSenderConfig {
    server: String,
    #[serde(default = "default_862")]
    port: u16,
    #[serde(default = "default_be")]
    dscp: String,
    n_packets: u64,
    // test_timeout: u64,
    model: String,
    // Auto-configured fields
}

impl Configurable<TWAMPSenderConfig> for TWAMPSenderConfig {
    fn get_config(
        cfg: &HashMap<String, serde_json::Value>,
    ) -> Result<TWAMPSenderConfig, Box<dyn Error>> {
        let mut filtered_cfg: HashMap<&str, &serde_json::Value> = HashMap::new();
        let mut model_cfg: HashMap<&str, &serde_json::Value> = HashMap::new();
        // Filter out config
        for (key, val) in cfg.iter() {
            if let Some(name) = key.strip_prefix("model_") {
                model_cfg.insert(name, val);
                continue;
            }
            filtered_cfg.insert(key, val);
        }
        // @todo: Model config
        // Continue as usual
        let c_value = serde_json::to_value(&filtered_cfg)?;
        match serde_json::from_value::<TWAMPSenderConfig>(c_value) {
            Ok(x) => Ok(x),
            Err(e) => Err(Box::new(e)),
        }
    }
}

pub type TWAMPSenderCollector = Collector<TWAMPSenderConfig>;

#[async_trait]
impl Collectable for TWAMPSenderCollector {
    async fn collect(&self) -> Result<Status, Box<dyn Error>> {
        // Convert dscp to numeric ToS
        let tos = dscp_to_tos(self.config.dscp.to_lowercase()).ok_or("invalid dscp")?;
        //
        log::debug!(
            "[{}] Connecting {}:{}",
            self.id,
            self.config.server,
            self.config.port
        );
        let stream =
            TcpStream::connect(format!("{}:{}", self.config.server, self.config.port)).await?;
        let mut session = TestSession::new_from(
            self.id.clone(),
            stream,
            tos,
            self.config.server.clone(),
            self.config.n_packets as u32,
        );
        session.run().await?;
        Ok(Status::Ok)
    }
}

struct TestSession {
    id: String,
    connection: Connection,
    tos: u8,
    reflector_addr: String,
    reflector_port: u16,
    n_packets: u32,
}

impl TestSession {
    pub fn new_from(
        id: String,
        stream: TcpStream,
        tos: u8,
        reflector_addr: String,
        n_packets: u32,
    ) -> TestSession {
        TestSession {
            id,
            connection: Connection::new(stream),
            tos,
            reflector_addr,
            reflector_port: 0,
            n_packets,
        }
    }
    pub fn set_reflector_port(&mut self, port: u16) {
        log::debug!("[{}] Setting reflector port to {}", self.id, port);
        self.reflector_port = port;
    }
    pub async fn run(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Connected", self.id);
        self.recv_server_greeting().await?;
        self.send_setup_reponse().await?;
        self.recv_server_start().await?;
        self.send_request_tw_session().await?;
        self.recv_accept_session().await?;
        self.send_start_sessions().await?;
        self.recv_start_ack().await?;
        self.run_test().await?;
        self.send_stop_sessions().await?;
        Ok(())
    }
    async fn recv_server_greeting(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Waiting for Server-Greeting", self.id);
        let sg: ServerGreeting = self.connection.read_frame().await?;
        log::debug!(
            "[{}] Server-Greeting received. Suggested modes: {}",
            self.id,
            sg.modes
        );
        if sg.modes == MODE_REFUSED {
            log::info!("[{}] Server refused connection. Stopping", self.id);
            return Err("session refused".into());
        }
        if sg.modes & MODE_UNAUTHENTICATED == 0 {
            log::info!("[{}] Unsupported mode. Stopping", self.id);
            return Err("unsupported mode".into());
        }
        Ok(())
    }
    async fn send_setup_reponse(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Sending Setup-Response", self.id);
        let sr = SetupResponse {
            mode: MODE_UNAUTHENTICATED,
            key_id: Bytes::copy_from_slice(DEFAULT_KEY_ID),
            token: Bytes::copy_from_slice(DEFAULT_TOKEN),
            client_iv: Bytes::copy_from_slice(DEFAULT_CLIENT_IV),
        };
        self.connection.write_frame(&sr).await?;
        Ok(())
    }
    async fn recv_server_start(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Waiting fot Server-Start", self.id);
        let ss: ServerStart = self.connection.read_frame().await?;
        log::debug!(
            "[{}] Server-Start received. Server timestamp: {}",
            self.id,
            ss.start_time,
        );
        Ok(())
    }
    async fn send_request_tw_session(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Sending Request-TW-Session", self.id);
        let srq = RequestTWSession {
            ipvn: 4,
            padding_length: 0,
            start_time: Utc::now(),
            timeout: 255, // @todo: Make configurable
            type_p: self.tos as u32,
        };
        self.connection.write_frame(&srq).await?;
        Ok(())
    }
    async fn recv_accept_session(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Waiting for Accept-Session", self.id);
        let acc_s: AcceptSession = self.connection.read_frame().await?;
        log::debug!(
            "[{}] Accept-Session Received. Reflector port: {}",
            self.id,
            acc_s.port
        );
        self.set_reflector_port(acc_s.port);
        Ok(())
    }
    async fn send_start_sessions(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Sending Start-Sessions", self.id);
        let req = StartSessions {};
        self.connection.write_frame(&req).await?;
        Ok(())
    }
    async fn recv_start_ack(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Waiting for Start-Ack", self.id);
        let resp: StartAck = self.connection.read_frame().await?;
        if resp.accept != ACCEPT_OK {
            log::error!(
                "[{}] Failed to start session. Accept code: {}",
                self.id,
                resp.accept
            );
            return Err("failed to start session".into());
        }
        log::debug!("[{}] Start-Ack Received. Accept: {}", self.id, resp.accept);
        Ok(())
    }
    async fn send_stop_sessions(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Sending Stop-Sessions", self.id);
        let req = StopSessions {
            accept: 0,
            num_sessions: 1,
        };
        self.connection.write_frame(&req).await?;
        Ok(())
    }
    async fn run_test(&mut self) -> Result<(), Box<dyn Error>> {
        log::debug!("[{}] Running test", self.id);
        let socket = UdpSocket::bind("0.0.0.0:0").await?;
        // Test request TTL must be set to 255
        socket.set_ttl(255)?;
        // @todo: Set IP_TOS
        let shared_socket = Arc::new(socket);
        let addr: SocketAddr =
            format!("{}:{}", self.reflector_addr, self.reflector_port).parse()?;
        //
        let (recv_result, sender_result) = tokio::join!(
            TestSession::run_test_receiver(self.id.clone(), shared_socket.clone(), self.n_packets),
            TestSession::run_test_sender(
                self.id.clone(),
                shared_socket.clone(),
                &addr,
                self.n_packets
            )
        );
        if let (Ok(r_stats), Ok(s_stats)) = (recv_result, sender_result) {
            TestSession::process_stats(s_stats, r_stats)
        }
        Ok(())
    }
    async fn run_test_sender(
        id: String,
        socket: Arc<UdpSocket>,
        addr: &SocketAddr,
        n_packets: u32,
    ) -> Result<SenderStats, &'static str> {
        match TestSession::test_sender(socket, addr, n_packets).await {
            Ok(r) => Ok(r),
            Err(e) => {
                log::error!("[{}] Sender error: {}", id, e);
                Err("sender error")
            }
        }
    }
    async fn run_test_receiver(
        id: String,
        socket: Arc<UdpSocket>,
        n_packets: u32,
    ) -> Result<ReceiverStats, &'static str> {
        match TestSession::test_receiver(socket, n_packets).await {
            Ok(r) => Ok(r),
            Err(e) => {
                log::error!("[{}] Receiver error: {}", id, e);
                Err("receiver error")
            }
        }
    }
    #[inline]
    async fn test_sender(
        socket: Arc<UdpSocket>,
        addr: &SocketAddr,
        n_packets: u32,
    ) -> Result<SenderStats, Box<dyn Error>> {
        let mut model = get_packet_model("g711")?;
        let mut buf = BytesMut::with_capacity(16384);
        let mut out_octets = 0usize;
        let t0 = Instant::now();
        let mut pkt_sent = 0u32;
        for s_seq in 0..n_packets {
            let pkt = model.next_packet();
            let next_deadline = tokio::time::Instant::now() + Duration::from_nanos(pkt.next_ns);
            let req = TestRequest {
                seq: s_seq,
                timestamp: Utc::now(),
                err_estimate: 0,
            };
            req.write_bytes(&mut buf)?;
            // @todo: Add Padding
            // let pad = pkt.size - 20 - 8 - buf.len(); // IP + UDP
            out_octets += socket.send_to(&buf, addr).await?;
            pkt_sent += 1;
            // Reset buffer pointer
            buf.clear();
            // Wait for next packet
            tokio::time::sleep_until(next_deadline).await;
        }
        Ok(SenderStats {
            pkt_sent,
            time_ns: t0.elapsed().as_nanos() as u64,
            out_octets,
        })
    }
    #[inline]
    async fn test_receiver(
        socket: Arc<UdpSocket>,
        n_packets: u32,
    ) -> Result<ReceiverStats, Box<dyn Error>> {
        // Stats
        let mut pkt_received = 0u32;
        // Roundtrip/Input/Output timings
        let mut rt_timing = Timing::new();
        let mut in_timing = Timing::new();
        let mut out_timing = Timing::new();
        // Roundtrip/Input/Output loss
        let mut in_loss = 0u32;
        let mut out_loss = 0u32;
        // Roundtrip/Input/Output hops
        let mut rt_min_hops = 0xffu16;
        let mut rt_max_hops = 0u16;
        let mut in_min_hops = 0xffu8;
        let mut in_max_hops = 0u8;
        let mut out_min_hops = 0xffu8;
        let mut out_max_hops = 0u8;
        // Octets
        let mut in_octets = 0usize;
        //
        let mut buf = BytesMut::with_capacity(16384);
        for count in 0..n_packets {
            let mut ts: UTCDateTime;
            // Try to read response,
            // @todo: Replace with UPDConnection
            loop {
                socket.readable().await?;
                ts = Utc::now();
                match socket.try_recv_buf(&mut buf) {
                    Ok(n) => {
                        in_octets += n + 20 + 8; // IP+UDP
                        break;
                    }
                    Err(ref e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                        continue;
                    }
                    Err(e) => {
                        return Err(Box::new(e));
                    }
                }
            }
            // Parse request
            let resp = TestResponse::parse(&mut buf)?;
            // Reset buffer pointer
            buf.clear();
            pkt_received += 1;
            // Amount of time spent inside reflector from receiving request to building response
            let reflector_delay = resp.timestamp - resp.recv_timestamp;
            // Amount of time spend on-fly in both directions
            // Measured as delta between received response and sending request,
            // except for reflector internal delay.
            let rt_delay = ts - resp.sender_timestamp - reflector_delay;
            rt_timing.register(rt_delay.num_nanoseconds().unwrap() as u64);
            // Estimate of inbound time,
            // Delta between sender timestamp and local time
            // @todo: Apply error estimate
            let in_delay = if ts >= resp.timestamp {
                ts - resp.timestamp
            } else {
                resp.timestamp - ts
            };
            in_timing.register(in_delay.num_nanoseconds().unwrap() as u64);
            // Estimate of outbound time,
            // Delta between sender timestamp and receiver timestamp
            // @todo: Apply error estimate
            let out_delay = if resp.recv_timestamp >= resp.sender_timestamp {
                resp.recv_timestamp - resp.sender_timestamp
            } else {
                resp.sender_timestamp - resp.recv_timestamp
            };
            out_timing.register(out_delay.num_nanoseconds().unwrap() as u64);
            // Detect loss
            in_loss = resp.seq - count;
            out_loss = resp.sender_seq - resp.seq;
            // @todo: register hops properly
            let out_hops = 255 - resp.sender_ttl;
            if out_hops > out_max_hops {
                out_max_hops = out_hops
            }
            if out_hops < out_min_hops {
                out_min_hops = out_hops
            }
            let in_hops = 0u8;
            if in_hops > in_max_hops {
                in_max_hops = in_hops
            }
            if in_hops < in_min_hops {
                in_min_hops = in_hops
            }
            let rt_hops = in_hops as u16 + out_hops as u16;
            if rt_hops > rt_max_hops {
                rt_max_hops = rt_hops
            }
            if rt_hops < rt_min_hops {
                rt_min_hops = rt_hops
            }
        }
        rt_timing.done();
        in_timing.done();
        out_timing.done();
        let rt_loss = n_packets - pkt_received;
        Ok(ReceiverStats {
            pkt_received,
            rt_timing,
            in_timing,
            out_timing,
            rt_loss,
            in_loss,
            out_loss,
            rt_min_hops,
            rt_max_hops,
            in_min_hops,
            in_max_hops,
            out_min_hops,
            out_max_hops,
            in_octets,
        })
    }
    fn process_stats(s_stats: SenderStats, r_stats: ReceiverStats) {
        let total = s_stats.pkt_sent as f64;
        log::debug!(
            "Packets sent: {pkt_sent}, Packets received: {pkt_recv}, Loss: {loss}, Duration: {duration}",
            pkt_sent = s_stats.pkt_sent,
            pkt_recv = r_stats.pkt_received,
            loss=0,
            duration=0
        );
        log::debug!(
            "Out octets: {out_octets} ({out_bitrate}), In octets: {in_octets} ({in_bitrate})",
            out_octets = s_stats.out_octets,
            in_octets = r_stats.in_octets,
            out_bitrate = 0,
            in_bitrate = 0,
        );
        log::debug!("Direction  | Min       | Max       | Avg       | Jitter    | Hops    | Loss");
        log::debug!(
            "-----------+-----------+-----------+-----------+-----------+---------+--------------"
        );
        log::debug!(
            "Inbound    | {min_delay:>9?} | {max_delay:?} | {avg_delay:?} | {jitter:?} | - | {loss:?}%",
            min_delay = Duration::from_nanos(r_stats.in_timing.min_ns),
            max_delay = Duration::from_nanos(r_stats.in_timing.max_ns),
            avg_delay = Duration::from_nanos(r_stats.in_timing.avg_ns),
            jitter = Duration::from_nanos(r_stats.in_timing.jitter_ns),
            loss = (r_stats.in_loss as f64) * 100.0 / total,
        );
        log::debug!(
            "Outbound   | {min_delay:?} | {max_delay:?} | {avg_delay:?} | {jitter:?} | - | {loss:?}%",
            min_delay = Duration::from_nanos(r_stats.out_timing.min_ns),
            max_delay = Duration::from_nanos(r_stats.out_timing.max_ns),
            avg_delay = Duration::from_nanos(r_stats.out_timing.avg_ns),
            jitter = Duration::from_nanos(r_stats.out_timing.jitter_ns),
            loss = (r_stats.in_loss as f64) * 100.0 / total,
        );
        log::debug!(
            "Round-Trip | {min_delay:?} | {max_delay:?} | {avg_delay:?} | {jitter:?} | - | {loss:?}%",
            min_delay = Duration::from_nanos(r_stats.rt_timing.min_ns),
            max_delay = Duration::from_nanos(r_stats.rt_timing.max_ns),
            avg_delay = Duration::from_nanos(r_stats.rt_timing.avg_ns),
            jitter = Duration::from_nanos(r_stats.rt_timing.jitter_ns),
            loss = (r_stats.in_loss as f64) * 100.0 / total,
        );
    }
}

#[derive(Debug)]
struct SenderStats {
    pkt_sent: u32,
    time_ns: u64,
    out_octets: usize,
}

#[derive(Debug)]
struct ReceiverStats {
    pkt_received: u32,
    // Roundtrip/Input/Output timings
    rt_timing: Timing,
    in_timing: Timing,
    out_timing: Timing,
    // Roundtrip/Input/Output loss
    rt_loss: u32,
    in_loss: u32,
    out_loss: u32,
    // Roundtrip/Input/Output hops
    rt_min_hops: u16,
    rt_max_hops: u16,
    in_min_hops: u8,
    in_max_hops: u8,
    out_min_hops: u8,
    out_max_hops: u8,
    // Octets
    in_octets: usize,
}

fn default_862() -> u16 {
    862
}

fn default_be() -> String {
    "be".into()
}

// Defaults
static DEFAULT_KEY_ID: &[u8] = &[
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
];
static DEFAULT_TOKEN: &[u8] = &[
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
];
static DEFAULT_CLIENT_IV: &[u8] = &[
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
];
