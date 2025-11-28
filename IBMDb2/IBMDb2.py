import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from ibm_db import connect

def IBMDb2(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://stackoverflow.com/questions/6044326/how-to-connect-python-to-db2
	
	conn = connect('DATABASE=' + inDatabase + ';'
					'HOSTNAME=' + os.environ["DBHost"] + ';'  # 127.0.0.1 or localhost works if it's local
					'PORT=' + os.environ["DBPort"] + ';'
					'PROTOCOL=TCPIP;'
					'UID=' + os.environ["DBUsername"] + ';'
					'PWD=' + os.environ["DBPassword"] + ';', '', '')

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")
	

dbName = "myDb"
tableName = "myTable"
IBMDb2( dbName, tableName )