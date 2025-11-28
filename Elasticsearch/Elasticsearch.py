import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

def ElasticSearch(inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://www.elastic.co/docs/explore-analyze/query-filter/languages/sql
	
	ELASTIC_PASSWORD = os.environ["DBPassword"]
	CLOUD_ID = os.environ["DBHost"]
	
	conn = Elasticsearch(
		cloud_id=CLOUD_ID,
		basic_auth=("elastic", ELASTIC_PASSWORD)
	)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")
	
tableName = "myTable"
ElasticSearch( tableName )