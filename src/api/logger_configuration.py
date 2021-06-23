import logging


def get_logger(name_logger: str) -> logging.Logger:
    format_log_output = (
        "%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
    )

    log = logging.getLogger(name=name_logger)
    log.setLevel(logging.INFO)

    if not log.handlers:
        log.addHandler(logger_stream_handler(format_log_output))

    log.propagate = False

    return log


def logger_stream_handler(format_log_output: str) -> logging.Handler:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(format_log_output))

    return stream_handler
