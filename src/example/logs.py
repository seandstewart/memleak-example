import logging.config
import typing as t

import structlog


def configure(
    *,
    level: str | int = None,
    filter_loggers: t.Iterable["str"] = (),
):
    """Configure logging for your application.

    Args:
        level: The minimum log-level for your logs. Should conform to standard python log levels.
        filter_loggers: Loggers to "filter" - i.e., raise to one level greater than the minimum.
    """

    shared, structured, renderer = _get_processors()
    formatting = {
        "()": structlog.stdlib.ProcessorFormatter,
        "processor": renderer,
        "foreign_pre_chain": shared,
    }
    level = logging.getLevelName(level) if isinstance(level, str) else level
    # we specify force because ddtrace messes with the root handler in a way
    # that screws up our logging, so we're force-resetting the root handler to
    # be what we want
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"default": formatting},
            "handlers": {
                "default": {
                    "level": level,
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": level,
                    "propagate": True,
                    "force": True,  # type: ignore[typeddict-item]
                }
            },
        }
    )
    for logger_name in filter_loggers:
        logging.getLogger(logger_name).setLevel(level + 10)

    structlog.configure(
        processors=shared + structured,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )



def _get_processors() -> tuple[list[t.Callable], list[t.Callable], t.Callable]:
    shared: list[t.Callable] = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.contextvars.merge_contextvars,
        structlog.processors.ExceptionPrettyPrinter()
    ]
    structured: list[t.Callable] = [
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter
    ]
    renderer = structlog.dev.ConsoleRenderer()
    return shared, structured, renderer
