---
---

# cpu Model Interface

CPU capabilities

## Variables

| Name          | Type        | Description                     | Required         | Constant         | Default |
| ------------- | ----------- | ------------------------------- | ---------------- | ---------------- | ------- |
| arch          | String      | Architecture:                   | :material-check: | :material-check: |         |
|               |             |                                 |                  |                  |         |
|               |             | * `x86`                         |                  |                  |         |
|               |             | * `x86_64`                      |                  |                  |         |
|               |             | * `PPC`                         |                  |                  |         |
|               |             | * `PPC64`                       |                  |                  |         |
|               |             | * `ARM7`                        |                  |                  |         |
|               |             | * `MIPS`                        |                  |                  |         |
| cores         | Integer     | Effective number of cores.      | :material-check: | :material-check: |         |
|               |             | For bigLITTLE and similar,      |                  |                  |         |
|               |             | effective number of cores is 2  |                  |                  |         |
|               |             | rather than 4                   |                  |                  |         |
| ht            | Boolean     | Hyper Theading support          | :material-close: | :material-check: |         |
| freq          | Integer     | Nominal frequence in MHz        | :material-close: | :material-check: |         |
| turbo_freq    | Integer     | Maximal frequence in MHz        | :material-close: | :material-check: |         |
| l1_cache      | Integer     | L1 cache size in kb             | :material-close: | :material-check: |         |
| l2_cache      | Integer     | L2 cache size in kb             | :material-close: | :material-check: |         |
| l3_cache      | Integer     | L3 cache size in kb             | :material-close: | :material-check: |         |
