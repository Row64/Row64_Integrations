import pandas as pd
import os
import sys
import oracledb
import paramiko
from scp import SCPClient

from row64tools import ramdb
from dotenv import load_dotenv

def OracleConnect():
	
	# Please set the following environment variables: DBHost, DBUsername, DBPassword to proper values.
	load_dotenv("C:\\r64tools\\db.env")
	
	# conn = oracledb.connect(user="C##radmin7", password="temp7", dsn="localhost/xepdb1")
	conn = oracledb.connect(user=os.getenv("DBUser"), password=os.getenv("DBPwd"), dsn=os.getenv("DBHost"))
	print("Successfully connected to Oracle Database")

	cursor = conn.cursor()
	cursor.execute("SELECT tdate,amount,product FROM sales")
	rows = cursor.fetchall()
	fields = cursor.description
	rList =  [{fields[i][0]:field_value for i, field_value in enumerate(v)} for v in rows]
	df = pd.DataFrame.from_records(rList)

	print(df) # prints dataframe, remove after testing

	# note this process seems to convert the column names to upper case
	
	# This example has a decimal type needed to be converted to to float
	df['AMOUNT'] = pd.to_numeric(df['AMOUNT'], errors='coerce')
	
	# example showing setting a column to datetime
	df["TDATE"] = pd.to_datetime(df["TDATE"])
	
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


OracleConnect()