import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from pyhive import hive

def ApacheHive(inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://stackoverflow.com/questions/21370431/how-to-access-hive-via-python
	try:
		conn = hive.Connection(host=os.environ["DBHost"], port=os.environ["DBPort"], username=os.environ["DBUsername"])
	except hive.Error as e:
		print(f"Error connecting to Database: {e}")
		sys.exit(1)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

tableName = "myTable"
ApacheHive( tableName )