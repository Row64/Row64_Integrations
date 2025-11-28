import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from impala.dbapi import connect

def ApacheImpala(inDatabase,inTablename):

	# Please set the following environment variables: DBHost. 
	# If you have a Kerberos auth on your Impala, DBUsername, DBPort to proper values, Uncomment the second line.
	load_dotenv()
	
	# Help page, https://impala.apache.org/docs/build/html/topics/impala_langref.html

	try:
		conn = connect(host=os.environ["DBHost"])
		
		# If you have a Kerberos auth on your Impala, you could use connection string like:
		# conn = connect(host=os.environ["DBHost"], port=os.environ["DBPort"], use_ssl=True,
		# database=inDatabase, user=os.environ["DBUsername"], kerberos_service_name='impala',
		# auth_mechanism = 'GSSAPI')
	except:
		print("Error connecting to Database")
		sys.exit(1)
		
	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
ApacheImpala( dbName, tableName )