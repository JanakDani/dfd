import fire
from libs import log4
from indices import indices
from libs import influxdb

logger = log4.patch()


class Update(object):
    def __init__(self, db_url: str, db_token: str, db_org: str,
                 log_level: str = "INFO", log_out: str = "stderr"):
        log4.set_logger(log_level, log_out)
        logger.info("Input args: db_url: " + db_url +
                    ", db_token: ********" +
                    ", db_org: " + db_org +
                    ", log_level: " + log_level +
                    ", log_file: " + log_out)
        logger.debug("setting up db client instance")
        self.influxdb_client = influxdb.InfluxDB(db_url, db_token, db_org)
        self.indices = indices.Indices(self.influxdb_client)

    def run(self):
        indices_output = self.indices.run()
        return indices_output


if __name__ == '__main__':
    fire.Fire(Update)
