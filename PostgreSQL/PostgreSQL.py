import pandas as pd
import os
import psycopg2
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def PostgreSQL(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://www.postgresqltutorial.com/postgresql-python/connect/
	
	try:
		conn = conn = psycopg2.connect(
			host=os.environ["DBHost"],
			database=inDatabase,
			user=os.environ["DBUsername"],
			password=os.environ["DBPassword"])
	except psycopg2.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
PostgreSQL( dbName, tableName )