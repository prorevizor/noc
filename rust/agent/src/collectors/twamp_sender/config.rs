// ---------------------------------------------------------------------
// twamp_sender collector configuration
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use crate::proto::pktmodel::ModelConfig;
use crate::proto::tos::dscp_to_tos;
use crate::zk::Configurable;
use serde::Deserialize;
use std::collections::HashMap;
use std::error::Error;

#[derive(Deserialize, Debug)]
pub struct TWAMPSenderConfig {
    pub server: String,
    #[serde(default = "default_862")]
    pub port: u16,
    #[serde(default = "default_be")]
    pub dscp: String,
    pub n_packets: usize,
    // test_timeout: u64,
    // Model config
    #[serde(flatten)]
    pub model: ModelConfig,
    // Internal fields
    #[serde(skip)]
    pub tos: u8,
}

impl Configurable<TWAMPSenderConfig> for TWAMPSenderConfig {
    fn get_config(
        cfg: &HashMap<String, serde_json::Value>,
    ) -> Result<TWAMPSenderConfig, Box<dyn Error>> {
        let c_value = serde_json::to_value(&cfg)?;
        let mut config = serde_json::from_value::<TWAMPSenderConfig>(c_value)?;
        // Fill internal fields
        config.tos = dscp_to_tos(config.dscp.to_lowercase()).ok_or("invalid dscp")?;
        Ok(config)
    }
}

fn default_862() -> u16 {
    862
}

fn default_be() -> String {
    "be".into()
}
