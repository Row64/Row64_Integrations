import pandas as pd
import os
import nzpy
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def IBMNetezza(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://docs.dominodatalab.com/en/latest/user_guide/5a641d/connect-to-ibm-netezza/#_credential_setup
	try:
		conn = nzpy.connect(user=os.environ["DBUsername"], password=os.environ["DBPassword"], host=os.environ["DBHost"], port=os.environ["DBPort"], database=inDatabase)
	except nzpy.Error as e:
		print(f"Error connecting to IBM Netezza Platform: {e}")
		sys.exit(1)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")
	

dbName = "myDb"
tableName = "myTable"
IBMNetezza( dbName, tableName )