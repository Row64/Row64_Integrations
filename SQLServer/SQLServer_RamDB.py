import pandas as pd
import os
import sys
import pyodbc
import paramiko
from scp import SCPClient

from row64tools import ramdb
from dotenv import load_dotenv
from pyodbc import connect

def SqlServer():
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv("C:\\r64tools\\db.env")
	
	# example showing database login with dotenv
	# conStr = 'Driver=ODBC Driver 17 for SQL Server;Server="' + os.getenv("DBHost") + '";'
	# conStr += 'Database="Examples";UID="' + os.getenv("DBUser") + '";'
	# conStr += ';PWD="' + os.getenv("DBPwd") + '";Trusted_Connection=yes;'
	# conn = pyodbc.connect(conStr)
	
	# example with simple windows login on localhost
	conn = pyodbc.connect('''Driver=ODBC Driver 17 for SQL Server;Server=localhost;Database=Examples;Trusted_Connection=yes;''')
	
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Sales")

	rows = cursor.fetchall()
	fields = cursor.description
	rList =  [{fields[i][0]:field_value for i, field_value in enumerate(v)} for v in rows]
	df = pd.DataFrame.from_records(rList)
	print(df) # prints dataframe, remove after testing

	# This example has a decimal type needed to be converted to to float
	df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	if os.path.isdir("C:\\r64tools"):
		local_path = "C:\\r64tools\\Test.ramdb"
		ramdb.save_from_df(df, local_path)
		remote_path = '/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb'
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			print("\n----- transfering .ramdb file -----")
			hostname = os.getenv("SSH_Host")
			port = os.getenv("SSH_Port")
			username = os.getenv("SSH_User")
			password = os.getenv("SSH_Pwd")
			ssh.connect(hostname=hostname, port=port, username=username, password=password)
			with SCPClient(ssh.get_transport()) as scp:
				scp.put(local_path, remote_path)
				print(".ramdb transfered successfully")
		except Exception as e:
			print(f"Error: {e}")
		finally:
			ssh.close()
	else:
		print("Folder C:\\r64tools not found, skipping save .ramdb")

	conn.close()


SqlServer()