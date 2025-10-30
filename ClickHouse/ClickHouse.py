import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from sqlalchemy import create_engine

def ClickHouse(inDatabase,inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://clickhouse.com/blog/querying-pandas-dataframes
	
	conn = create_engine('clickhouse://' + os.environ["DBUsername"] + ':@' + os.environ["DBHost"] + '/' + inDatabase)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

dbName = "myDb"
tableName = "myTable"
ClickHouse( dbName, tableName )