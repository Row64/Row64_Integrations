import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from databricks import sql

def Databricks(inTablename):

	# Please set the following environment variables: DATABRICKS_SERVER_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN to proper values.
	
	load_dotenv()
	
	# Help page, https://docs.databricks.com/aws/en/dev-tools/python-sql-connector
	
	with sql.connect(server_hostname   = os.getenv("DATABRICKS_SERVER_HOSTNAME"),
                 http_path         = os.getenv("DATABRICKS_HTTP_PATH"),
                 access_token      = os.getenv("DATABRICKS_TOKEN"),
                 user_agent_entry = "product_name") as connection:
    
    with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM " + inTablename)

    records0 = cursor.fetchall()
	fields = cursor.description
	rList =  [{fields[i][0]:field_value for i, field_value in enumerate(v)} for v in records0]
	df = pd.DataFrame.from_records(rList)

	# example showing setting decimal type converted to to float
	# df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

tableName = "myTable"
Databricks( tableName )