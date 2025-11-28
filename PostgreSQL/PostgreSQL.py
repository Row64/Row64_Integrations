import pandas as pd
import os
import psycopg2
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def PostgreSQL(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv("/home/row64/r64tools/db.env")
	
	# Help page, https://www.postgresqltutorial.com/postgresql-python/connect/
	
	print("DBHost:",os.environ["DBHost"])
	print("inDatabase:",inDatabase)
	print("DBUsername:",os.environ["DBUsername"])
	print("DBPassword:",os.environ["DBPassword"])
	try:
		conn = conn = psycopg2.connect(
			host=os.environ["DBHost"],
			database=inDatabase,
			user=os.environ["DBUsername"],
			password=os.environ["DBPassword"])
	except psycopg2.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)

	print("Connected to PostgreSQL")
	cur = conn.cursor()
	cur.execute("SELECT * FROM " + inTablename)

	df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

	print(df) # print out example dataframe, remove this for any production use

	# This example has a decimal type needed to be converted to to float
	df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


	cur.close()
	conn.close()


dbName = "examples"
tableName = "sales"
PostgreSQL( dbName, tableName )