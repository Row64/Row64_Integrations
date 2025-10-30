import pandas as pd
import os
import mysql.connector
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def MySQL(inDatabase,inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://dev.mysql.com/doc/connector-python/en/
	
	try:
		conn = mysql.connector.connect(user=os.environ["DBUsername"], 
							password=os.environ["DBPassword"],
							host=os.environ["DBHost"],
							database=inDatabase)
	except mysql.connector.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
MySQL( dbName, tableName )