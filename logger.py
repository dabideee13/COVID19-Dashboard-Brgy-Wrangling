import logging

# Log configurations
LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
)
LOG_FORMATTER = logging.Formatter(
    LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_LEVEL = logging.DEBUG

MAIN_LOG_FILE = "main.log"
main_logger = logging.getLogger('main')
main_logger.setLevel(LOG_LEVEL)

# Main logger (file)
main_logger_file_handler = logging.FileHandler(MAIN_LOG_FILE)
main_logger_file_handler.setLevel(LOG_LEVEL)
main_logger_file_handler.setFormatter(LOG_FORMATTER)
main_logger.addHandler(main_logger_file_handler)

# Main logger (console)
stream_logger = logging.getLogger('stream')
stream_logger.setLevel(LOG_LEVEL)
stream_logger_stream_handler = logging.StreamHandler()
stream_logger_stream_handler.setLevel(LOG_LEVEL)
stream_logger_stream_handler.setFormatter(LOG_FORMATTER)
stream_logger.addHandler(stream_logger_stream_handler)

