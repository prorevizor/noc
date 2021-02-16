// ---------------------------------------------------------------------
// Packet model
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use std::error::Error;

/// Address family
#[derive(Debug)]
pub enum AFI {
    IPv4,
    IPv6,
}

impl AFI {
    pub fn from_address(address: &str) -> Result<AFI, Box<dyn Error>> {
        match address.find("::") {
            Some(_) => Ok(AFI::IPv6),
            None => Ok(AFI::IPv4),
        }
    }
}

/// Packet for modeling
#[derive(Debug)]
pub struct Packet {
    pub size: usize,
    pub next_ns: u64,
}

pub trait PacketModel {
    fn next_packet(&mut self) -> Packet;
}

pub const NS: u64 = 1_000_000_000;
