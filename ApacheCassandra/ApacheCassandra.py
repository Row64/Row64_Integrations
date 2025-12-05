import os
import pandas as pd
from row64tools import ramdb
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import paramiko
from scp import SCPClient

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)

def ApacheCassandra():

	load_dotenv("/home/row64/r64tools/db.env")
	
	print("-------- Before connection --------")
	cluster = Cluster(
	    contact_points=['127.0.0.1'], 
	    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
	)
	session = cluster.connect()
	print("-------- Connection Success! --------")

	session.row_factory = pandas_factory
	session.default_fetch_size = None
	
	query = "SELECT * FROM store.sales"
	rslt = session.execute(query, timeout=None)
	df = rslt._current_rows

	df["date"] = pd.to_datetime(df["date"])
	print(df)

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

ApacheCassandra()