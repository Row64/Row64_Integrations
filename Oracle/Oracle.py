import pandas as pd
import os
import cx_Oracle
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def Oracle(inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Example, https://www.geeksforgeeks.org/oracle-database-connection-in-python/
	
	try:
		conn = cx_Oracle.connect(os.environ["DBUsername"] + '/' + os.environ["DBPassword"] + '@' + os.environ["DBHost"] + ':' + os.environ["DBPort"] + '/xe')
	except cx_Oracle.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


tableName = "myTable"
Oracle( tableName )