import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from pyhive import presto

def Presto(inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://stackoverflow.com/questions/55988436/how-to-convert-a-presto-query-output-to-a-python-data-frame
	
	try:
		conn = presto.connect(host=os.environ["DBHost"], port=os.environ["DBPort"], protocol='https', username=os.environ["DBUsername"], password=os.environ["DBPassword"])
	except presto.Error as e:
		print(f"Error connecting to Presto Platform: {e}")
		sys.exit(1)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


tableName = "myTable"
Presto( tableName )