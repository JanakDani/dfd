import sys
import json
import socket
from loguru import logger

logger.remove(0)
hostname = socket.gethostname()
ipAddress = socket.gethostbyname(hostname)


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "level": record["level"].name,
        "source": {
            "hostname": hostname,
            "ipAddress": ipAddress,
            "pid": record["process"].id,
            "file": record["file"].path,
            "module": record["module"],
            "function": record["function"],
            "name": record["name"],
            "line": record["line"]
        },
        "message": record["message"],
        "exception": record["exception"]
    }
    return json.dumps(subset)


def custom_record(record):
    record["extra"]["serialized"] = serialize(record)


def patch():
    return logger.patch(custom_record)


def set_console_logger(log_level: str = "INFO"):
    # logger.remove(0)
    logger.add(sys.stderr, level=log_level, diagnose=False, enqueue=True, catch=True,
               format="{extra[serialized]}")


def set_file_logger(log_level: str, log_file: str):
    # logger.remove(0)
    logger.add(log_file, level=log_level, diagnose=False, enqueue=True, catch=True,
               format="{extra[serialized]}")


def set_logger(log_level: str = "INFO", log_out: str = "stderr"):
    if log_out == "stderr":
        set_console_logger(log_level)
    else:
        set_file_logger(log_level, log_out)
