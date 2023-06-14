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
                "time": self.start_epoch
            }
            list_data.append(dict_data)
        return list_data

    def write(self):
        self.influxdb_client.write(self.influxdb_bucket, self.data_for_influxdb())

    def run(self):
        self.write()
