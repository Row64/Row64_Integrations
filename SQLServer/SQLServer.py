import pandas as pd
import os
import pymssql
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def OpenServer(inDatabase,inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://docs.microsoft.com/en-us/sql/connect/python/pymssql/step-3-proof-of-concept-connecting-to-sql-using-pymssql?view=sql-server-ver16

	try:
		conn = pymssql.connect(server=os.environ["DBHost"], user=os.environ["DBUsername"], password=os.environ["DBPassword"], database=inDatabase)
	except pymssql.Error as e:
		print(f"Error connecting to SQL Server Platform: {e}")
		sys.exit(1)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
OpenServer( dbName, tableName )