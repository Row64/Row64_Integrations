import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from sqlalchemy import create_engine

def AscendIO(inDatabase,inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://developer.ascend.io/docs/sql-functions

	conn = create_engine('ascend://' + os.environ["DBUsername"] + ':' + os.environ["DBPassword"] + '@' + os.environ["DBHost"] + ':' + os.environ["DBPort"] + '/' + inDatabase + '?auth_mechanism=PLAIN;use_ssl=true')

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
AscendIO( dbName, tableName )