// ---------------------------------------------------------------------
// PacketModel registry
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use super::PacketModel;
use super::G711;
use std::error::Error;

pub fn get_packet_model(name: &str) -> Result<impl PacketModel, Box<dyn Error>> {
    match name {
        "g711" => Ok(G711 {}),
        _ => Err(format!("Unknown packet model: {}", name).into()),
    }
}
