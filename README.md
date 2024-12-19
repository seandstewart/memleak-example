# memleak-example

This is an example aiohttp app meant to demonstrate the memory leak present in current versions
of ddtrace-py.

## Usage

### Intallation

```shell
make install
```

### Run the server

> **note:** If you want to export telemetry, be sure to set your `DD_API_KEY` in your .env.

```shell
make serve
```