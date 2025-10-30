import pandas as pd
import os
import sqlalchemy as sa
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def ApacheKylin(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://kylin.apache.org/docs/3.1.3/tutorial/sql_reference/

	conn = sa.create_engine('kylin://' + os.environ["DBUsername"] + ':' + os.environ["DBPassword"] + '@' + os.environ["DBHost"] + ':' + os.environ["DBPort"] + '/' + inDatabase,
	connect_args={'is_ssl': True, 'timeout': 60})
	
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
ApacheKylin( dbName, tableName )