import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from firebolt.db import connect

def Firebolt(inDatabase,inTablename):
	
	# Please set the following environment variables: DBEngine, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://python-sdk.docs.firebolt.io/en/latest/Connecting_and_queries.html
	
	conn = connect(
			engine_name=os.environ["DBEngine"],
			database=inDatabase,
			username=os.environ["DBUsername"],
			password=os.environ["DBPassword"],)

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
Firebolt( dbName, tableName )