import os, time
from influxdb_client_3 import InfluxDBClient3, Point

token = "InR7yqiHQAQNVmR1od6IVpGoHu-BoFT2Qjd6L7-zH_TCGloL0iFTOoegZWo3ragfgravEZ57itww-l16GrxG_Q=="
org = "Test"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = InfluxDBClient3(host=host, token=token, org=org)

# database="StockData"
# query = """SELECT *
# FROM 'census'
# WHERE time >= now() - interval '24 hours'
# AND ('bees' IS NOT NULL OR 'ants' IS NOT NULL)"""
#
# # Execute the query
# table = client.query(query=query, database="StockData", language='sql')
#
# # Convert to dataframe
# df = table.to_pandas().sort_values(by="time")
# print(df)



