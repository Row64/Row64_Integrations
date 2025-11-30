import pandas as pd
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from row64tools import ramdb

def Create_Example_Parquet(inPath):

	data = {
	"Date": ["2025-01-21 13:23:44","2025-01-21 13:23:52","2025-01-21 13:24:03","2025-01-21 13:24:17"],
	"Amount": [446.57,287.24,1376.28,3200.10],
	"Product": ["Seal SE Robotic Pool Vacuum","Tikom Robot Vacuum and Mop","ECOVACS DEEBOT T20 Omni Robot Vacuum","Husqvarna Automower 430XH"],
	}
	df = pd.DataFrame(data)
	table = pa.Table.from_pandas(df)
	pq.write_table(table, inPath)

def Parquet_To_Ramdb(inPath, inRamDbPath):
	
	table = pq.read_table(inPath)
	df = table.to_pandas()

	print(df) # print out example dataframe, remove this for any production use

	# example showing setting a column to datetime
	df["Date"] = pd.to_datetime(df["Date"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	# ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")
	ramdb.save_from_df(df, inRamDbPath)
	print("----------------------------")
	print("Saved .ramdb to:", inRamDbPath)
	

parquetPath = 'test.parquet'
ramdbPath = 'test.ramdb'

Create_Example_Parquet(parquetPath)
Parquet_To_Ramdb(parquetPath, ramdbPath)