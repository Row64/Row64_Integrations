import pandas as pd
import os
import psycopg2
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def YugabyteDB(inDatabase,inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://docs.yugabyte.com/preview/develop/tutorials/build-apps/python/cloud-ysql-python/
	
	try:
		connString = "host="+ os.environ["DBHost"] +" port="+ os.environ["DBPort"] +" dbname="+ inDatabase +" user="+ os.environ["DBUsername"] +" password="+ os.environ["DBPassword"] +"     load_balance=True"

		conn = psycopg2.connect(connString)
	except psycopg2.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
YugabyteDB( dbName, tableName )