import sys
import socket
import json
import fire
from loguru import logger
from indices import indices


class CustomLog(object):
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)

    @staticmethod
    def serialize(record):
        subset = {
            "timestamp": record["time"].timestamp(),
            "level": record["level"].name,
            "source": {
                "hostname": CustomLog.hostname,
                "ipAddress": CustomLog.ipAddress,
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

    @staticmethod
    def patching(record):
        record["extra"]["serialized"] = CustomLog.serialize(record)

    @staticmethod
    def set_logger(log_level, log_file):
        if log_file:
            logger.add(log_file, level=log_level, diagnose=False, enqueue=True, catch=True,
                       format="{extra[serialized]}")
        else:
            logger.add(sys.stderr, level=log_level, diagnose=False, enqueue=True, catch=True,
                       format="{extra[serialized]}")


class Pipeline(object):
    def __init__(self, log_level: str = "INFO", log_file: str = None):
        CustomLog.set_logger(log_level, log_file)
        self.indices = indices.IndicesStage

    def run(self):
        print(dir(self.indices))
        logger.debug("this is a debug message")
        logger.info("this is a info message")


if __name__ == '__main__':
    logger.remove(0)
    logger = logger.patch(CustomLog.patching)
    fire.Fire(Pipeline)
