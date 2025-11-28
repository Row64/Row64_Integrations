import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from pinotdb import connect

def ApachePinot(inTablename):

	# Please set the following environment variables: DBHost, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://docs.pinot.apache.org/users/clients/python
	conn = connect(host=os.environ["DBHost"], port=os.environ["DBPort"], path='/query/sql', scheme='http')
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")

tableName = "myTable"
ApachePinot( tableName )