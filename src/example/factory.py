import aiohttp.web

import ddtrace
from ddtrace.contrib import aiohttp as tracing

from example import views
from vendor import middlewares


def create_app(vendored: bool = False) -> aiohttp.web.Application:
    app = aiohttp.web.Application()
    app.router.add_view("/", views.SampleView)
    if vendored:
        middlewares.trace_app(app=app, tracer=ddtrace.tracer)
        return app

    tracing.trace_app(app=app, tracer=ddtrace.tracer)
    return app