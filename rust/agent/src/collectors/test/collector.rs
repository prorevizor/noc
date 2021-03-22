// ---------------------------------------------------------------------
// test collector implementation
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------
use super::TestConfig;
use crate::collectors::base::{Collectable, Collector, Status};
use async_trait::async_trait;
use std::error::Error;

pub type TestCollector = Collector<TestConfig>;

#[async_trait]
impl Collectable for TestCollector {
    async fn collect(&self) -> Result<Status, Box<dyn Error>> {
        Ok(Status::Ok)
    }
}
