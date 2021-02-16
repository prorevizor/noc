// ---------------------------------------------------------------------
// G.711 packet model
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use super::{Packet, PacketModel, NS};

pub struct G711;

impl PacketModel for G711 {
    fn next_packet(&mut self) -> Packet {
        Packet {
            size: 20 + 8 + 12 + 160, // IP + UDP + RTP + Payload
            next_ns: NS / 50,        // 50 pps
        }
    }
}
