from spx import SPX
from libs import log4
from libs import influxdb

logger = log4.patch()


class Indices(object):
    def __init__(self, influxdb_client, influxdb_bucket: str = "indices"):
        self.influxdb_client = influxdb_client
        self.influxdb_bucket = influxdb_bucket
        self.start_epoch, self.end_epoch = influxdb.InfluxDB.time()
        self.influxdb_data = None

    def run(self):
        self.write()

    def data_for_influxdb(self):
        list_data = []
        spx = SPX()
        for cik, symbol, company, weight, sector, sub_industry in spx.data_for_indices():
            dict_data = {
                "measurement": "spx",
                "tags": {
                    "type": "index",
                    "symbol": symbol,
                    "resolution": "weekly"
                },
                "fields": {
                    "cik": cik,
                    "company": company,
                    "weight": weight,
                    "sector": sector,
                    "subIndustry": sub_industry
                },
                "time": self.end_epoch
            }
            list_data.append(dict_data)
        return list_data

    def write(self):
        """
        list_data = []
        start_epoch, end_epoch = influxdb.InfluxDB.time()
        logger.debug("invoking S&P 500 instance")
        spx = SPX()
        for cik, symbol, company, weight, sector, sub_industry in spx.stocks_details():
            dict_data = {
                "measurement": "spx",
                "tags": {
                    "type": "index",
                    "symbol": symbol,
                    "resolution": "weekly"
                },
                "fields": {
                    "cik": cik,
                    "company": company,
                    "weight": weight,
                    "sector": sector,
                    "subIndustry": sub_industry
                },
                "time": end_epoch
            }
            list_data.append(dict_data)
        """
            # print(dict_data)
            # influxdb.write("indices", dict_data)

        # json_data = json.dumps(list_data)
        self.influxdb_data = self.data_for_influxdb()
        #json_data = self.influxdb_data
        print(self.influxdb_data)
        self.influxdb_client.write(self.influxdb_bucket, self.influxdb_data)
