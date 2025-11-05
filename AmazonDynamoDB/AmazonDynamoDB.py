import pandas as pd
import os

from row64tools import ramdb
from dotenv import load_dotenv
from dynamo_pandas import put_df, get_df, keys

def AmazonDynamoDB(inDbName, inTableName):
	
	# for this example we just show loading a dynamodb s3 file saved locally
	df = pd.DataFrame()
	with open(r'/home/row64/local-dynamodb-file') as s3:
	    for item in s3:
	        newdf = pd.read_json(item)
	        newdf.fillna(method='ffill', inplace=True)
	        newdf = newdf.loc['s']
	        df = df.append(newdf, ignore_index=True)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])

	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

dbName = "myDb"
tableName = "myTable"
AmazonDynamoDB( dbName, tableName )