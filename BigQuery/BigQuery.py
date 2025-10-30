import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account

def BigQuery(inCredential,inProjectID,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://www.rudderstack.com/guides/how-to-access-and-query-your-bigquery-data-using-python-and-r

	credentials = service_account.Credentials.from_service_account_file(
	inCredential)

	project_id = inProjectID
	conn = bigquery.Client(credentials= credentials,project=project_id)
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


credential = "/path/to/Credential.json"
projectID = "ProjectID"
tableName = "Tablename"
BigQuery( credential, projectID, tableName )