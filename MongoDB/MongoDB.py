import pandas as pd
import os
import sys
from row64tools import ramdb
from dotenv import load_dotenv
from pymongo import MongoClient
import paramiko
from scp import SCPClient

def MongoDB():

	load_dotenv("/home/row64/r64tools/db.env")
	
	client = MongoClient("mongodb://localhost:27017/")

	database = client["example"]
	col = database["sales"]
	df = pd.DataFrame(list(col.find({}, {'_id': False})))


	df["Date"] = pd.to_datetime(df["Date"])

	print(df)
	print('os.getenv("SSH_Host"): ', os.getenv("SSH_Host"))
	print('os.getenv("SSH_User"): ', os.getenv("SSH_User"))
	print('os.getenv("SSH_Pwd"): ', os.getenv("SSH_Pwd"))

	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	if os.path.isdir("/home/row64/r64tools/"):
		local_path = "/home/row64/r64tools/Test.ramdb"
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
		print("Folder /home/row64/r64tools/ not found, skipping save .ramdb")
MongoDB()