import pandas as pd
import os
import mariadb
import sys

from row64tools import ramdb
from dotenv import load_dotenv

def Mariadb(inDatabase,inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values, may have to change port value.
	load_dotenv()
	
	# Help page, https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
	
	try:
		conn = mariadb.connect(
			user=os.environ["DBUsername"],
			password=os.environ["DBPassword"],
			host=os.environ["DBHost"],
			port=3306,
			database=inDatabase
		)
	except mariadb.Error as e:
		print(f"Error connecting to MariaDB Platform: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")
	

dbName = "myDb"
tableName = "myTable"
Mariadb( dbName, tableName )