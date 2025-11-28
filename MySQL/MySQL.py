import pandas as pd
import os
import mysql.connector
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def MySQL(inDatabase,inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv("/home/row64/r64tools/db.env")
	
	# Help page, https://dev.mysql.com/doc/connector-python/en/
	
	try:
		conn = mysql.connector.connect(user=os.environ["DBUsername"], 
							password=os.environ["DBPassword"],
							host=os.environ["DBHost"],
							database=inDatabase)
	except mysql.connector.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)

	print("Connected to mysql")
	
	# cursor -> list -> dataframe is much faster than SQLAlchemy
	# but you might have to do some extra work explicity setting the column types
	cursor= conn.cursor()
	cursor.execute("SELECT * FROM " + inTablename)
	records0 = cursor.fetchall()
	fields = cursor.description
	rList =  [{fields[i][0]:field_value for i, field_value in enumerate(v)} for v in records0]
	df = pd.DataFrame.from_records(rList)
	
	# This example has a decimal type needed to be converted to to float
	df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
	
	print(df) # print out example dataframe, remove this for any production use
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


dbName = "Examples"
tableName = "Sales"
MySQL( dbName, tableName )