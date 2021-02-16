// ---------------------------------------------------------------------
// TWAMP Test-Request structure
// ---------------------------------------------------------------------
// Copyright (C) 2007-2021 The NOC Project
// See LICENSE for details
// ---------------------------------------------------------------------

use super::{NTPTimeStamp, UTCDateTime};
use crate::proto::frame::{FrameError, FrameReader, FrameWriter};
use bytes::{Buf, BufMut, BytesMut};

/// ## Test-Request structure
/// RFC-4656: 4.1.2
/// NB: Unauthorized mode only
/// ```text
///  0                   1                   2                   3
///  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
/// +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/// |                        Sequence Number                        |
/// +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/// |                          Timestamp                            |
/// |                                                               |
/// +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/// |        Error Estimate         |                               |
/// +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               |
/// |                                                               |
/// .                                                               .
/// .                         Packet Padding                        .
/// .                                                               .
/// |                                                               |
/// +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
/// ```
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct TestRequest {
    pub seq: u32,
    pub timestamp: UTCDateTime,
    pub err_estimate: u16,
    // padding
}

impl FrameReader for TestRequest {
    fn min_size() -> usize {
        14
    }
    fn parse(s: &mut BytesMut) -> Result<TestRequest, FrameError> {
        // Sequence number, 4 octets
        let seq = s.get_u32();
        // Timestamp, 8 octets
        let ts = NTPTimeStamp::new(s.get_u32(), s.get_u32());
        // Err estimate, 2 octets
        let err_estimate = s.get_u16();
        Ok(TestRequest {
            seq,
            timestamp: ts.into(),
            err_estimate,
        })
    }
}

impl FrameWriter for TestRequest {
    /// Get size of serialized frame
    fn size(&self) -> usize {
        14
    }
    /// Serialize frame to buffer
    fn write_bytes(&self, s: &mut BytesMut) -> Result<(), FrameError> {
        // Sequence number, 4 octets
        s.put_u32(self.seq);
        // Timestamp, 8 octets
        let ts: NTPTimeStamp = self.timestamp.into();
        s.put_u32(ts.secs());
        s.put_u32(ts.fracs());
        // Err estimate, 2 octets
        s.put_u16(self.err_estimate);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use crate::proto::frame::{FrameReader, FrameWriter};
    use crate::proto::twamp::TestRequest;
    use bytes::{Buf, BytesMut};
    use chrono::{TimeZone, Utc};

    static TEST_REQUEST: &[u8] = &[
        0x00, 0x00, 0x04, 0x00, // Sequence, 4 octets
        0xe3, 0xd0, 0xd0, 0x20, 0x00, 0x00, 0x00, 0x00, // Timestamp, 8 octets
        0x00, 0x0f, // Err estimate, 2 octets
    ];

    fn get_test_request() -> TestRequest {
        TestRequest {
            seq: 1024,
            timestamp: Utc.ymd(2021, 2, 12).and_hms(10, 0, 0),
            err_estimate: 15,
        }
    }

    #[test]
    fn test_test_request_min_size() {
        assert_eq!(TestRequest::min_size(), 14);
    }

    #[test]
    fn test_test_request_parse() {
        let mut buf = BytesMut::from(TEST_REQUEST);
        let expected = get_test_request();
        let res = TestRequest::parse(&mut buf);
        assert_eq!(buf.remaining(), 0);
        assert_eq!(res, Ok(expected))
    }

    #[test]
    fn test_test_request_size() {
        let sg = get_test_request();
        assert_eq!(sg.size(), 14)
    }

    #[test]
    fn test_test_request_write_bytes() {
        let msg = get_test_request();
        let mut buf = BytesMut::with_capacity(msg.size());
        let res = msg.write_bytes(&mut buf);
        assert!(res.is_ok());
        assert_eq!(buf.split(), BytesMut::from(TEST_REQUEST));
    }
}
