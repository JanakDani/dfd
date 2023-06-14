from libs import log4
import pytz
import datetime
from isoweek import Week
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

logger = log4.patch()


class InfluxDB(object):
    def __init__(self, db_url, db_token, db_org):
        self.db_url = db_url
        self.db_token = db_token
        self.db_org = db_org
        self.client = influxdb_client.InfluxDBClient(url=self.db_url, token=self.db_token, org=self.db_org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    @staticmethod
    def time():
        logger.debug("deriving time in epoch (seconds)")
        timezone = pytz.timezone('US/Eastern')
        year, week, weekday = datetime.date.today().isocalendar()
        monday = Week(year, week).monday()
        friday = Week(year, week).friday()
        week_start_datetime = timezone.localize(datetime.datetime(monday.year, monday.month, monday.day, 2, 0, 0))
        week_end_datetime = timezone.localize(datetime.datetime(friday.year, friday.month, friday.day, 22, 0, 0))
        week_start_epoch = int(week_start_datetime.timestamp())
        week_end_epoch = int(week_end_datetime.timestamp())
        # print(datetime.datetime.fromtimestamp(week_start_epoch))
        # print(datetime.datetime.fromtimestamp(week_end_epoch))
        logger.debug("week_start_epoch:{:f}, week_end_epoch={:f}", week_start_epoch, week_end_epoch)
        return week_start_epoch, week_end_epoch

    def write(self, bucket, record):
        self.write_api.write(bucket, self.db_org, record,
                             write_precision=influxdb_client.domain.write_precision.WritePrecision.S)

        """
        print(dir(resp))
        query_api = self.client.query_api()
        query = 'from(bucket:"indices") |> range(start: -1d)'
        result = query_api.query(org=self.db_org, query=query)
        print(result)
        """
