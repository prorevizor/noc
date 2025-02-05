# twamp_sender collector

`twamp_sender` connects to [`twamp_reflector`](twamp_reflector.md) and performs
TWAMP SLA probe using one of the predefined [packet models](#packet-models).

## Configuration

| Parameter   | Type             | Default       | Description                                                                                 |
| ----------- | ---------------- | ------------- | ------------------------------------------------------------------------------------------- |
| `id`        | String           |               | Collector's ID. Must be unique per agent instance. Will be returned along with the metrics. |
| `type`      | String           |               | Must be `twamp_sender`                                                                      |
| `service`   | String           | Equal to `id` | Service id for output metrics                                                               |
| `interval`  | Integer          |               | Repetition interval in seconds                                                              |
| `labels`    | Array of Strings |               | List of additional labels. Will be returned along with metrics                              |
|             |                  |               |                                                                                             |
| `server`    | String           |               |                                                                                             |
| `port`      | Integer          | `862`         |                                                                                             |
| `dscp`      | String           | `be`          |                                                                                             |
| `n_packets` | Integer          |               |                                                                                             |
| `model`     | String           |               | Name of the [packet model](#packet-models)                                                  |

### Packet Models

#### G.711

G.711 voice session imitation.

| Parameter | Type   | Description    |
| --------- | ------ | -------------- |
| `model`   | String | Must me `g711` |

#### G.729

G.729 voice session imitation.

| Parameter | Type   | Description    |
| --------- | ------ | -------------- |
| `model`   | String | Must me `g729` |

#### CBR

Constant bitrate session, filling required bandwidth by packets of required size.

| Parameter         | Type   | Description                     |
| ----------------- | ------ | ------------------------------- |
| `model`           | String | Must me `cbr`                   |
| `model_bandwidth` | String | Required bandwidth, bit/s       |
| `model_size`      | String | Required packet size, in octets |

#### IMIX

Internet MIX (IMIX) packet model. Filling required bandwidth by most-commonly
observed packets sizes.

| Parameter         | Type   | Description               |
| ----------------- | ------ | ------------------------- |
| `model`           | String | Must me `cbr`             |
| `model_bandwidth` | String | Required bandwidth, bit/s |

Packet distribution:

| Packet size | Packets | Distribution (packets) | Bytes | Distribution (bytes) |
| ----------: | ------: | ---------------------: | ----: | -------------------: |
|          70 |       7 |                 58.33% |   490 |               11.41% |
|         576 |       4 |                 33.33% |  2304 |               53.65% |
|        1500 |       1 |                  8.33% |  1500 |               34.94% |

!!! note

    TWAMP protocol doesn't allow test packets under the 70 octets.
    So provided model uses small packets of bigger size and
    resulting distribution slightly differs from commonly used
    IMIX models.

## Collected Metrics

| Metric             | Metric Type | Platform | Description        |
| ------------------ | ----------- | -------- | ------------------ |
| `ts`               |             | All      | ISO 8601 Timestamp |
| `collector`        |             | All      | Collector Id       |
| `labels`           |             | All      | List of labels     |
|                    |             |          |                    |
| `tx_packets`       |             | All      |                    |
| `rx_packets`       |             | All      |                    |
| `tx_bytes`         |             | All      |                    |
| `rx_bytes`         |             | All      |                    |
| `duration_ns`      |             | All      |                    |
| `tx_pps`           |             | All      |                    |
| `rx_pps`           |             | All      |                    |
| `tx_bitrate`       |             | All      |                    |
| `rx_bitrate`       |             | All      |                    |
| **Inbound**        |             |          |                    |
| `in_min_delay_ns`  |             | All      |                    |
| `in_max_delay_ns`  |             | All      |                    |
| `in_avg_delay_ns`  |             | All      |                    |
| `in_jitter_ns`     |             | All      |                    |
| `in_loss`          |             | All      |                    |
| **Outbound**       |             |          |                    |
| `out_min_delay_ns` |             | All      |                    |
| `out_max_delay_ns` |             | All      |                    |
| `out_avg_delay_ns` |             | All      |                    |
| `out_jitter_ns`    |             | All      |                    |
| `out_loss`         |             | All      |                    |
| **Round-trip**     |             |          |                    |
| `rt_min_delay_ns`  |             | All      |                    |
| `rt_max_delay_ns`  |             | All      |                    |
| `rt_avg_delay_ns`  |             | All      |                    |
| `rt_jitter_ns`     |             | All      |                    |
| `rt_loss`          |             | All      |                    |

## Compilation Features

Enable `twamp-sender` feature during compiling the agent (Enabled by default).
