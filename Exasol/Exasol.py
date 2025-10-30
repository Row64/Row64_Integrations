import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from sqlalchemy import create_engine

def Exasol(inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://docs.exasol.com/db/latest/sql_reference.htm

	conn = create_engine('exa+pyodbc://' + os.environ["DBUsername"] + ':' + os.environ["DBPassword"] + '@' + os.environ["DBHost"] + ':' + os.environ["DBPort"] + '/my_schema?CONNECTIONLCALL=en_US.UTF-8&driver=EXAODBC')

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")
	

tableName = "myTable"
Exasol( tableName )