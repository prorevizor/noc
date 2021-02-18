// ---------------------------------------------------------------------
// Packet model
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use serde::Deserialize;

/// Packet for modeling
#[derive(Debug, PartialEq)]
pub struct Packet {
    pub seq: usize,
    pub size: usize,
    pub next_ns: u64,
}

// Nanosecond
const NS: u64 = 1_000_000_000;

#[derive(Deserialize, Debug, Clone, Copy)]
#[serde(rename_all = "lowercase")]
#[serde(tag = "model")]
pub enum ModelConfig {
    /// G.711 voip session model
    G711,
    /// G.729 voip session model
    G729,
    /// Constant bitrate session model
    /// Sends packets of `size` at pps `rate`
    CBR {
        #[serde(rename = "model_bandwidth")]
        bandwidth: usize,
        #[serde(rename = "model_size")]
        size: usize,
    },
    /// IMix model
    /// Send packets of variable size utilizing `bandwidth` (bits/s)
    IMIX {
        #[serde(rename = "model_bandwidth")]
        bandwidth: usize,
    },
}

/// PPS model:
/// Fixed packet `size` at `pps` rate
pub fn get_pps_model(size: usize, pps: usize) -> Box<dyn Fn(usize) -> Packet + Send> {
    let next_ns = NS / pps as u64;
    Box::new(move |seq| Packet { seq, size, next_ns })
}

/// IMIX iterator.
/// Implements IMIX Simple model.
/// Yields 7 packets of 40 octets, 4 of 576 and one for 1500.
const IMIX1: usize = 40;
const IMIX1_COUNT: usize = 7;
const IMIX2: usize = 576;
const IMIX2_COUNT: usize = 4;
const IMIX3: usize = 1500;
const IMIX3_COUNT: usize = 1;
const IMIX_SAMPLE_COUNT: usize = IMIX1_COUNT + IMIX2_COUNT + IMIX3_COUNT;
static IMIX_SAMPLE: &[usize; 12] = &[
    IMIX1, IMIX2, IMIX1, IMIX2, IMIX1, IMIX2, IMIX1, IMIX2, IMIX1, IMIX1, IMIX1, IMIX3,
];
pub fn get_imix_model(bandwidth: usize) -> Box<dyn Fn(usize) -> Packet + Send> {
    const IMIX_ROUND: u64 =
        ((IMIX1_COUNT * IMIX1 + IMIX2_COUNT * IMIX2 + IMIX3_COUNT * IMIX3) * 8) as u64;
    let next_ns = NS * IMIX_ROUND / (bandwidth * IMIX_SAMPLE_COUNT) as u64;
    Box::new(move |seq| Packet {
        seq,
        size: IMIX_SAMPLE[seq % IMIX_SAMPLE_COUNT],
        next_ns,
    })
}

//
impl ModelConfig {
    /// Create iterator yielding `Packet` according the model
    pub fn get_model(self) -> Box<dyn Fn(usize) -> Packet + Send> {
        match self {
            Self::G711 => get_pps_model(20 + 8 + 12 + 160, 50),
            Self::G729 => get_pps_model(20 + 8 + 12 + 20, 50),
            Self::CBR { bandwidth, size } => get_pps_model(size, bandwidth / (size * 8)),
            Self::IMIX { bandwidth } => get_imix_model(bandwidth),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::{ModelConfig, Packet};

    #[test]
    fn test_g711_model() {
        let get_packet = ModelConfig::G711.get_model();
        let pkt = get_packet(0);
        let expected = Packet {
            seq: 0,
            size: 200,
            next_ns: 20_000_000,
        };
        assert_eq!(pkt, expected);
    }
    #[test]
    fn test_g729_model() {
        let get_packet = ModelConfig::G729.get_model();
        let pkt = get_packet(0);
        let expected = Packet {
            seq: 0,
            size: 60,
            next_ns: 20_000_000,
        };
        assert_eq!(pkt, expected);
    }
}
