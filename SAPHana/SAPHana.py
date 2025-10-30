import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from hdbcli import dbapi

def SAPHana(inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://developers.sap.com/tutorials/hana-clients-python.html
	
	try:
		conn = dbapi.connect(
			#Option 1, retrieve the connection parameters from the hdbuserstore
			#key='USER1UserKey', # address, port, user and password are retrieved from the hdbuserstore

			#Option2, specify the connection parameters
			address=os.environ["DBHost"],
			port=os.environ["DBPort"],
			user=os.environ["DBUsername"],
			password=os.environ["DBPassword"],

			#Additional parameters
			#encrypt=True, # must be set to True when connecting to HANA as a Service
			#As of SAP HANA Client 2.6, connections on port 443 enable encryption by default (HANA Cloud)
			#sslValidateCertificate=False #Must be set to false when connecting
			#to an SAP HANA, express edition instance that uses a self-signed certificate.
		)
	except dbapi.Error as e:
		print(f"Error connecting to SAP Hana Platform: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


tableName = "myTable"
SAPHana( tableName )