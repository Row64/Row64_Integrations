import pandas as pd
import os

from row64tools import ramdb
from dotenv import load_dotenv
from pydrill.client import PyDrill

def ApacheDrill(inTablename):

	# Please set the following environment variables: DBHost, DBPort to proper values.
	load_dotenv()
	
	# Help page, https://pypi.org/project/pydrill/
	drill = PyDrill(host=os.environ["DBHost"], port=os.environ["DBPort"])

	result = drill.query("SELECT * FROM" + inTablename)

	df = result.to_dataframe()
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

tableName = "myTable"
ApacheDrill( tableName )