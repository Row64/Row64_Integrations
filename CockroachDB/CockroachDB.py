import pandas as pd
import os
import psycopg2
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def CockroachDB(inDbName, inTableName):

	# Please set the following environment variables: DBHost, DBUsername, fill python ssl and certs to proper values.
	load_dotenv()
	
	# Help page, https://www.cockroachlabs.com/docs/v21.1/connect-to-the-database-cockroachcloud?filters=python
	try:

		conn = psycopg2.connect(
			database = inDbName,
			user = os.environ["DBUsername"],
			password = os.environ["DBPassword"],
			sslmode = 'require',
			sslrootcert = 'certs/ca.crt',
			sslkey = 'certs/client.maxroach.key',
			sslcert = 'certs/client.maxroach.crt',
			port = 26257,
			host = os.environ["DBHost"],
			
		)
	except psycopg2.Error as e:
		print(f"Error connecting to database: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTableName, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
CockroachDB( dbName, tableName )