import pandas as pd
import os
import gspread
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

def GoogleSheets(inCredential,inDatabase):
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv()
	
	# Help page, https://medium.com/@Bwhiz/step-by-step-guide-importing-google-sheets-data-into-pandas-ae2df899257f
	
	scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]

	credentials = ServiceAccountCredentials.from_json_keyfile_name(inCredential, scope)
	client = gspread.authorize(credentials)
	
	sheet = client.open(inDatabase).sheet1
	data = sheet.get_all_records()

	df = pd.DataFrame(data)
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


credential = "/path/to/Credential.json"
database = "DbName"
BigQuery( credential, database )