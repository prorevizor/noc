# twamp_sender collector

`twamp_sender` collects and records the necessary information provided from the packets transmitted by the Session-Reflector for measuring two-way metrics.


## Configuration

| Parameter   | Type             | Default | Description                                                                                 |
| ----------- | ---------------- | ------- | ------------------------------------------------------------------------------------------- |
| `id`        | String           |         | Collector's ID. Must be unique per agent instance. Will be returned along with the metrics. |
| `type`      | String           |         | Must be `twamp_sender`                                                                      |
| `interval`  | Integer          |         | Repetition interval in seconds                                                              |
| `labels`    | Array of Strings |         | List of additional labels. Will be returned along with metrics                              |
|             |                  |         |                                                                                             |
| `server`    | String           |         |                                                                                             |
| `port`      | u16,             | 862     |                                                                                             |
| `dscp`      | String           | be      |                                                                                             |
| `n_packets` | usize            |         |                                                                                             |
| `model`     |                  |         |                                                                                             |


## Collected Metrics

| Metric             | Metric Type | Platform | Description        |
| ------------------ | ----------- | -------- | ------------------ |
| `ts`               |             | All      | ISO 8601 Timestamp |
| `collector`        |             | All      | Collector Id       |
| `labels`           |             | All      | List of labels     |
|                    |             |          |                    |
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
|    **Inbound**     |             |          |                    |
| `in_min_delay_ns`  |             | All      |                    |
| `in_max_delay_ns`  |             | All      |                    |
| `in_avg_delay_ns`  |             | All      |                    |
| `in_jitter_ns`     |             | All      |                    |
| `in_loss`          |             | All      |                    |
|    **Outbound**    |             |          |                    |
| `out_min_delay_ns` |             | All      |                    |
| `out_max_delay_ns` |             | All      |                    |
| `out_avg_delay_ns` |             | All      |                    |
| `out_jitter_ns`    |             | All      |                    |
| `out_loss`         |             | All      |                    |
|    **Round-trip**  |             |          |                    |
| `rt_min_delay_ns`  |             | All      |                    |
| `rt_max_delay_ns`  |             | All      |                    |
| `rt_avg_delay_ns`  |             | All      |                    |
| `rt_jitter_ns`     |             | All      |                    |
| `rt_loss`          |             | All      |                    |


`twamp_sender` collector appends following labels

| Label              | Description       |
| ------------------ | ----------------- |
| `noc::dev::{name}` | Block device name |


## Compilation Features

Enable `twamp_sender` feature during compiling the agent (Enabled by default).
