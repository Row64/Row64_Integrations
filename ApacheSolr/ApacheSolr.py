import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from sqlalchemy import create_engine

def ApacheSolr(inDatabase,inServerPath,Tablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://solr.apache.org/guide/solr/latest/query-guide/sql-query.html
	
	conn = create_engine('solr://' + os.environ["DBUsername"] + ':' + os.environ["DBPassword"] + '@' + os.environ["DBHost"] + ':' + os.environ["DBPort"] + '/' + inServerPath + '/' + inDatabase)

	df = pd.read_sql_query("SELECT * FROM " + Tablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

dbName = "myDb"
serverPath = "/opt/solr/bin/solr"
tableName = "myTable"
ApacheSolr( dbName, serverPath, tableName )