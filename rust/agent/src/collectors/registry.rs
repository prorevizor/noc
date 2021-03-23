// ---------------------------------------------------------------------
// Collectors registry
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------
use super::dns::{DNSCollector, DNSConfig};
use super::test::{TestCollector, TestConfig};
use super::twamp_reflector::{TWAMPReflectorCollector, TWAMPReflectorConfig};
use super::twamp_sender::{TWAMPSenderCollector, TWAMPSenderConfig};
use super::Runnable;
use crate::zk::ZkConfigCollector;
use serde::Deserialize;
use std::error::Error;

#[derive(Deserialize, Debug, Clone)]
#[serde(tag = "type")]
pub enum CollectorConfig {
    #[serde(rename = "dns")]
    DNSCollector(DNSConfig),
    #[serde(rename = "test")]
    TestCollector(TestConfig),
    #[serde(rename = "twamp_reflector")]
    TWAMPReflectorCollector(TWAMPReflectorConfig),
    #[serde(rename = "twamp_sender")]
    TWAMPSenderCollector(TWAMPSenderConfig),
}

impl CollectorConfig {
    pub fn get_collector(
        config: &ZkConfigCollector,
    ) -> Result<Box<dyn Runnable + Send + Sync>, Box<dyn Error>> {
        match config.config.clone() {
            CollectorConfig::DNSCollector(c) => Ok(Box::new(DNSCollector::new_from(config, c)?)),
            CollectorConfig::TestCollector(c) => Ok(Box::new(TestCollector::new_from(config, c)?)),
            CollectorConfig::TWAMPReflectorCollector(c) => {
                Ok(Box::new(TWAMPReflectorCollector::new_from(config, c)?))
            }
            CollectorConfig::TWAMPSenderCollector(c) => {
                Ok(Box::new(TWAMPSenderCollector::new_from(config, c)?))
            }
        }
    }
}
