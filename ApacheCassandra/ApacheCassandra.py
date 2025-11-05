import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)

def ApacheCassandra(inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://stackoverflow.com/questions/73639095/how-to-connect-to-cassandra-database-using-python-code
	
	cluster = Cluster(['10.1.2.3'], port=45678)
	session = cluster.connect()
	
	session.row_factory = pandas_factory
	session.default_fetch_size = None
	
	query = "SELECT * FROM " + inTablename
	rslt = session.execute(query, timeout=None)
	df = rslt._current_rows

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

tableName = "myTable"
ApacheCassandra( tableName )