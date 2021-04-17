import os
import logging
import logging.handlers

from . import __FUNGITDIR__

FMT_NORMAL = logging.Formatter(
    fmt="%(asctime)s %(levelname).4s %(message)s", datefmt="%H:%M:%S"
)
FMT_DEBUG = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d %(levelname).4s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)


def ensure_path(file_name: str) -> str:
    if not os.path.exists(file_name):
        dir_path = "/".join(file_name.split("/")[:-1])
        os.makedirs(dir_path, exist_ok=True)


def setup_logging(debug=False, log_file=__FUNGITDIR__ + "/log/fungit.log"):
    root_logger = logging.getLogger()

    if debug:
        log_level = logging.DEBUG
        formatter = FMT_DEBUG
    else:
        log_level = logging.INFO
        formatter = FMT_NORMAL

    if log_file:
        if log_file == "-":
            log_handle = logging.StreamHandler()
        else:
            ensure_path(log_file)
            try:
                log_handle = logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=1048576, backupCount=4
                )
            except PermissionError:
                print(f'No permission to write to "{log_file}" directory!')
                raise SystemExit(1)

    log_handle.setFormatter(formatter)
    log_handle.setLevel(log_level)

    root_logger.addHandler(log_handle)
    root_logger.setLevel(0)
