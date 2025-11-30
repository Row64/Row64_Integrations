import pandas as pd
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from row64tools import ramdb


def Csv_To_Ramdb(inCsvPath, inRamDbPath):
	
	df = pd.read_csv(inCsvPath)
	print(df) # print out example dataframe, remove this for any production use
	
	# example showing setting a column to datetime
	df["Date"] = pd.to_datetime(df["Date"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	# ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")
	ramdb.save_from_df(df, inRamDbPath)
	print("----------------------------")
	print("Saved .ramdb to:", inRamDbPath)
	

csvPath = 'Sales.csv'
ramdbPath = 'Test.ramdb'

Csv_To_Ramdb(csvPath, ramdbPath)