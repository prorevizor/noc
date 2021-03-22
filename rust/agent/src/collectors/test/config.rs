// ---------------------------------------------------------------------
// test collector configuration
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use crate::zk::Configurable;
use serde::Deserialize;

#[derive(Deserialize)]
pub struct TestConfig {}

impl Configurable<TestConfig> for TestConfig {}
