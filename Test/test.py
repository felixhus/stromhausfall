# from datetime import datetime
#
# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS
#
# # You can generate an API token from the "API Tokens Tab" in the UI
# token = "xzrzW89eptcGAAgx4IRWMrtXZkyRqhnajYW5E5qihMgSO1LUUwf3_-Qo7kQSpxFAy5p0DQ9Y-FVayr5TgmhSqg=="
# org = "PowerHouse"
# bucket = "Testbucket"
#
# with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
#     write_api = client.write_api(write_options=SYNCHRONOUS)
#
#     sequence = ["mem,host=host1 used_percent=23.43234543",
#                 "mem,host=host1 available_percent=15.856523"]
#     write_api.write(bucket, org, sequence)
#
# client.close()
#
from datetime import datetime

from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086)
client.create_database('testdatabase')
client.get_list_database()
client.switch_database('testdatabase')
