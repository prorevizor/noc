// ---------------------------------------------------------------------
// twamp-reflector collector
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

mod config;
pub use config::TwampReflectorConfig;

cfg_if::cfg_if! {
    if #[cfg(feature = "twamp-reflector")] {
        mod collector;
        pub use collector::TwampReflectorCollector;
    } else {
        use super::StubCollector;
        pub type TwampReflectorCollector = StubCollector<TwampReflectorConfig>;
    }
}
