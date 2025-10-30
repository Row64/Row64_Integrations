import pandas as pd
import os
import teradatasql
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def Teradata(inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://stackoverflow.com/questions/35938320/connecting-python-with-teradata-using-teradata-module

	with teradatasql.connect(host=os.environ["DBHost"], user=os.environ["DBUsername"], password=os.environ["DBPassword"]) as conn:

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


tableName = "myTable"
Teradata( tableName )