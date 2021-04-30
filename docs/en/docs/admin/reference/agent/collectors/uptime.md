# uptime collector

`uptime` collects total running time.


## Configuration

| Parameter  | Type             | Default | Description                                                                                 |
| ---------- | ---------------- | ------- | ------------------------------------------------------------------------------------------- |
| `id`       | String           |         | Collector's ID. Must be unique per agent instance. Will be returned along with the metrics. |
| `type`     | String           |         | Must be `uptime`                                                                            |
| `interval` | Integer          |         | Repetition interval in seconds                                                              |
| `labels`   | Array of Strings |         | List of additional labels. Will be returned along with metrics                              |


## Collected Metrics

| Metric          | Metric Type | Platform | Description        |
| --------------- | ----------- | -------- | ------------------ |
| `ts`            |             | All      | ISO 8601 Timestamp |
| `collector`     |             | All      | Collector Id       |
| `labels`        |             | All      | List of labels     |
|                 |             |          |                    |
| `uptime`        |             | All      |                    |


`uptime` collector appends following labels

| Label              | Description       |
| ------------------ | ----------------- |
| `noc::dev::{name}` | Block device name |


## Compilation Features

Enable `uptime` feature during compiling the agent (Enabled by default).
