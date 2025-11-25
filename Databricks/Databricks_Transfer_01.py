import paramiko
from scp import SCPClient

remote_path = 'mkdir -p /var/www/ramdb/loading/RAMDB.Row64/Temp/test.ramdb'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	print("\n----- transfering .ramdb file -----")
	hostname = "192.168.1.10"
	port = 22
	username = "row64"
	password = "temp7"
	ssh.connect(hostname=hostname, port=port, username=username, password=password)
	with SCPClient(ssh.get_transport()) as scp:
		scp.put("test.ramdb", remote_path)
		print(".ramdb transfered successfully")
except Exception as e:
	print(f"Error: {e}")
finally:
	ssh.close()


