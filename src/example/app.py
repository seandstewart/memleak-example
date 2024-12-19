#!/usr/bin/env python3
import dotenv

dotenv.load_dotenv()

import ddtrace.auto
import ddtrace.profiling.auto
import ddtrace.runtime

import os
import typing

import faker
import aiohttp.web
import uvloop

from example import factory, logs

def run() -> typing.NoReturn:
    ddtrace.runtime.RuntimeMetrics.enable()
    logs.configure(level=10)
    vendored = os.environ.get('TRACE_PROVIDER', 'vendored').lower() == 'vendored'
    host = os.environ.get('SERVER_HOST', '0.0.0.0')
    port = int(os.environ.get('SERVER_PORT', 8080))
    app = factory.create_app(vendored=vendored)
    app["fake"] = faker.Faker()
    aiohttp.web.run_app(
        app, host=host, port=port, loop=uvloop.new_event_loop()
    )

if __name__ == '__main__':
    run()
