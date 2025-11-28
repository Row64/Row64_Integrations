import pandas as pd
import os
import psycopg2
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def AmazonRedshift(inDbName, inTableName):
	
	# Please set the following environment variables: DBHost, DBPort, DBUsername, and DBPassword
	load_dotenv()
	
	# Help page, https://docs.aws.amazon.com/redshift/latest/mgmt/python-connect-integrate-pandas.html
	
	try:
		conn = psycopg2.connect(
			dbname = inDbName,
			host = os.environ["DBHost"],
			port = os.environ["DBPort"],
			user = os.environ["DBUsername"],
			password = os.environ["DBPassword"]
		)
	except psycopg2.Error as e:
		print(f"Error connecting to database: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTableName, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])

	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")

dbName = "myDb"
tableName = "myTable"
AmazonRedshift( dbName, tableName )