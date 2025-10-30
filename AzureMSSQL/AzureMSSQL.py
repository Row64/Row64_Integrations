import pandas as pd
import os
import mysql.connector
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def AzureMSSQL(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.  Also add path to ssl in python.
	load_dotenv()
	
	# Help page, https://docs.microsoft.com/en-us/azure/mysql/single-server/connect-python
	
	try:
		user = os.environ["DBUsername"] + '@' + os.environ["DBHost"]
		host = os.environ["DBHost"] + '.mysql.database.azure.com'
		conn = mysql.connector.connect({'host':host,
		'user':user,
		'password':os.environ["DBPassword"],
		'database':inDatabase,
		'client_flags': [mysql.connector.ClientFlag.SSL],
		'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'})

	except mysql.connector.Error as e:
		print(f"Error connecting to Azure MS SQL Platform: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


dbName = "myDb"
tableName = "myTable"
AzureMSSQL( dbName, tableName )