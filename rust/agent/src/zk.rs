// ---------------------------------------------------------------------
// ZkConfig
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use crate::collectors::CollectorConfig;
use serde::Deserialize;
use std::error::Error;

#[derive(Deserialize, Debug)]
pub struct ZkConfig {
    #[serde(rename = "$version")]
    _version: String,
    #[serde(rename = "$type")]
    _type: String,
    pub config: ZkConfigConfig,
    pub collectors: Vec<ZkConfigCollector>,
}

#[derive(Deserialize, Debug)]
pub struct ZkConfigConfig {
    pub zeroconf: ZkConfigConfigZeroconf,
}

#[derive(Deserialize, Debug)]
pub struct ZkConfigConfigZeroconf {
    pub interval: u64,
}

#[derive(Deserialize, Debug)]
pub struct ZkConfigCollector {
    pub id: String,
    // #[serde(rename = "type")]
    // pub collector_type: String,
    pub interval: u64,
    #[serde(default)]
    pub disabled: bool,
    #[serde(flatten)]
    pub config: CollectorConfig,
}

impl ZkConfig {
    pub fn new_from(data: Vec<u8>) -> Result<Self, Box<dyn Error>> {
        match serde_json::from_slice(data.as_slice()) {
            Ok(x) => Ok(x),
            Err(e) => {
                log::error!("Cannot parse JSON: {}", e);
                Err("Cannot parse JSON".into())
            }
        }
    }
}
