import structlog
import logging
import sys

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s", stream=sys.stdout,
    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S'
)
structlog.configure(
    processors=[
        structlog.processors.KeyValueRenderer(
            key_order=["event"]
        )
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
)

ADDRESS = 'ipc:///tmp/mas'
NUM_OF_WORKERS = 4
