import pandas as pd
import os
import trino
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def Trino(inTablename):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPort, DBSchema, DBCatalog to proper values.
	load_dotenv()

	# Help page, https://github.com/trinodb/trino-python-client
	
	conn = trino.dbapi.connect(
		host=os.environ["DBHost"],
		port=os.environ["DBPort"],
		user=os.environ["DBUsername"],
		catalog=os.environ["DBCatalog"],
		schema=os.environ["DBSchema"],
	)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


tableName = "myTable"
Trino( tableName )