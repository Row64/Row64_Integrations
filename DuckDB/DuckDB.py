import pandas as pd
import duckdb

from row64tools import ramdb
from dotenv import load_dotenv

def DuckDB(inDbName,inTablename):
	
	# Help page, https://duckdb.org/docs/stable/sql/introduction
	
	conn = duckdb.connect(inDbName)

	df = duckdb.sql("SELECT * FROM " + inTablename).df()
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")

	
dbName = "data/example.db"
DuckDB( dbName, tableName )