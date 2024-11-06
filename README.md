# tomato-psutil
`tomato` driver for the [`psutil`](https://github.com/giampaolo/psutil) library.

This driver illustrates how a device driver can be implemented for devices which have no components. The driver is developed by the [ConCat lab at TU Berlin](https://tu.berlin/en/concat).

## Supported functions

### Capabilities
- `mem_info`: returns memory-related information
- `cpu_info`: returns CPU-related information
- `all_info`: returns all available information

### Attributes
- `mem_total`: the total physical memory installed, `RO`, `float`
- `mem_avail`: the available physical memory, `RO`, `float`
- `mem_usage`: the percentage of available physical memory, `RO`, `float`
- `cpu_count`: the number of logical CPUs, `RO`, `int`
- `cpu_freq`: the current frequency of the CPU (OS and CPU dependent), `RO`, `float`
- `cpu_usage`: the percentage of CPU usage, `RO`, `float`

## Contributors
- Peter Kraus
