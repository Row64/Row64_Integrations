import os
import subprocess as sp

'''===========================================================

TEST Setup for MySQL Python Integration into Row64

To execute using the 'python' (the non-OS python & will ask for sudo password):
python TEST_SETUP_MySQL.py

Assumes:
- run in a Ubuntu 24.04 / 25.04 VM or clean install
- you ran Setup_pyenv.py (makes a python that can pip install)

Process:
 - will setup a .env folder in /user/row64/r64tools
 - will install MySQL with test users
 - will setup needed pip libraries for MySQL connector
 - will setup an example .env file with: login, password, etc

==========================================================='''

def Setup_Env_Folder():
    # this folder will store the integration .env with passwords, etc
    # you can modify it to your custom location - this is just an example
    sp.call(['bash', '-c', "mkdir /home/row64/r64tools"])
    sp.call(['bash', '-c', "chown -R row64:row64 /home/row64/r64tools/"])
    sp.call(['bash', '-c', "chmod -R 777 /home/row64/r64tools/"]) # temp lower permission for MySQL access

    # if row64server is not installed, or if the live structure is not in place - make the folders
    if not os.path.exists("/var/www/ramdb/"):
        sp.call(["sudo", 'bash', '-c', "mkdir -p /var/www/ramdb/live/RAMDB.Row64/Temp"])
        sp.call(["sudo", 'bash', '-c', "chown -R row64:row64 /var/www/ramdb/"])
    elif not os.path.exists("/var/www/ramdb/live/RAMDB.Row64/"):
        sp.call(["sudo", 'bash', '-c', "mkdir -p /var/www/ramdb/live/RAMDB.Row64/Temp"])
        sp.call(["sudo", 'bash', '-c', "chown -R row64:row64 /var/www/ramdb/live/RAMDB.Row64"])
    elif not os.path.exists("/var/www/ramdb/live/RAMDB.Row64/Temp"):  
        sp.call(["sudo", 'bash', '-c', "mkdir -p /var/www/ramdb/live/RAMDB.Row64/Temp"])
        sp.call(["sudo", 'bash', '-c', "chown -R row64:row64 /var/www/ramdb/live/RAMDB.Row64/Temp"])

    
def MySQL_Install():
    
    tDir = '/usr/Row64/temp'
    sp.call(["sudo","apt","install","-y","mysql-server"])
    sp.call(["sudo","apt","install","-y","libmysqlclient-dev"])
    
    
    sqlTxt = """CREATE USER 'admin'@'localhost' IDENTIFIED BY 'AdminSetup7';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE Examples;
USE Examples;
CREATE TABLE Sales (Date DATETIME, Amount DECIMAL(15,2), Product VARCHAR(50));
INSERT INTO Sales VALUES ("2025-01-21 13:23:44", 446.57, "Seal SE Robotic Pool Vacuum");
INSERT INTO Sales VALUES ("2025-01-21 13:23:52", 287.24, "Tikom Robot Vacuum and Mop");
INSERT INTO Sales VALUES ("2025-01-21 13:24:03", 1376.28, "ECOVACS DEEBOT T20 Omni Robot Vacuum");
INSERT INTO Sales VALUES ("2025-01-21 13:24:17", 3200.10, "Husqvarna Automower 430XH");
""" 

    sqPath = '/home/row64/r64tools/sqlSetup.sql'
    f = open(sqPath, "w")
    f.write(sqlTxt)
    f.close()
    os.system("sudo mysql -sfu root < \"/home/row64/r64tools/sqlSetup.sql\"")

    ''' if you want to print the test data in the terminal, type:
            sudo mysql
            USE Examples;
            SELECT * FROM Sales; 
    '''

def Pip_Install():
    
    r64env = os.environ.copy()
    r64env["PYENV_ROOT"] = f"/home/row64/.pyenv"
    r64env["PATH"] = f"/home/row64/.pyenv/bin:{r64env['PATH']}"
    
    # pip install mysql-connector-python

    '''from the terminal, pip install in pyenv would look like:
        pip install row64tools
        pip install pandas
        pip install python-dotenv
        pip install mysql-connector-python
    '''

# pip install mysql-connector-python

    pipStr = """pip install row64tools
pip install pandas
pip install python-dotenv
pip install mysql-connector-python
"""
    
    pipSPath = "/home/row64/r64tools/pipSetup.sh"
    f = open(pipSPath, "w")
    f.write(pipStr)
    f.close()
    os.chmod(os.path.join(pipSPath), 0o0777)
    sp.call(['bash', '-c',pipSPath], env=r64env)

    # we can call the current python with /home/row64/.pyenv/shims/python


def Security_Setup():

    # for security we make a .env file with a example database credentials
    # be sure to replace with your own private credentials 
    
    envPath = "/home/row64/r64tools/db.env"
    envStr = """DBHost=localhost
DBUsername=admin
DBPassword=AdminSetup7"""
    
    f = open(envPath, "w")
    f.write(envStr)
    f.close()
    os.chmod(os.path.join(envPath), 0o0777)
    

Setup_Env_Folder()
MySQL_Install()
Pip_Install()
Security_Setup()