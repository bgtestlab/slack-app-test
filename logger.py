import logging

LOG_LEVEL = "INFO"


def logger():
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return log


LOG = logger()
LOG.debug(f"Starting with log level: {LOG_LEVEL}")
