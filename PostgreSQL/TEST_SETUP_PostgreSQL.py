import os
import subprocess as sp

'''===========================================================

TEST Setup for PostgreSQL Python Integration into Row64

To execute using the 'python' (the non-OS python & will ask for sudo password):
python TEST_SETUP_PostgreSQL.py

Assumes:
- run in a Ubuntu 24.04 / 25.04 VM or clean install
- you ran Setup_pyenv.py (makes a python that can pip install)

Process:
 - will setup a .env folder in /user/row64/r64tools
 - will install PostgreSQL with test users
 - will setup needed pip libraries for PostgreSQL connector
 - will setup an example .env file with: login, password, etc

==========================================================='''

def Setup_Env_Folder():
    # this folder will store the integration .env with passwords, etc
    # you can modify it to your custom location - this is just an example
    sp.call(['bash', '-c', "mkdir /home/row64/r64tools"])
    sp.call(['bash', '-c', "chown -R row64:row64 /home/row64/r64tools/"])
    sp.call(['bash', '-c', "chmod -R 777 /home/row64/r64tools/"]) # temp lower permission for PostgreSQL access

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

def PostgreSQL_Install():
    
    tDir = '/usr/Row64/temp'
    sp.call(["sudo","apt","install","-y","postgresql"])
    sp.call(["sudo","apt","install","-y","libpq-dev"])
    
    # Create test user, database and example data
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -c "CREATE DATABASE examples;"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "CREATE TABLE sales (date TIMESTAMP, amount DECIMAL(15,2), product VARCHAR(50));"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "CREATE USER admin WITH PASSWORD 'AdminSetup7';"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "GRANT CONNECT ON DATABASE examples TO admin;"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO admin;"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "GRANT ALL ON SCHEMA public TO admin;"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "INSERT INTO sales (date, amount, product) VALUES ('2025-01-21 13:23:44', 446.57, 'Seal SE Robotic Pool Vacuum');"'''])
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "INSERT INTO sales (date, amount, product) VALUES ('2025-01-21 13:23:52', 287.24, 'Tikom Robot Vacuum and Mop');"'''])    
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "INSERT INTO sales (date, amount, product) VALUES ('2025-01-21 13:24:03', 1376.28, 'ECOVACS DEEBOT T20 Omni Robot Vacuum');"'''])    
    sp.call(["sudo", 'bash', '-c', '''sudo -u postgres psql -d "examples" -c "INSERT INTO sales (date, amount, product) VALUES ('2025-01-21 13:24:17', 3200.10, 'Husqvarna Automower 430XH');"'''])    
    
    ''' To log the example database in the terminal:
            sudo -u postgres psql -d "examples"
            SELECT * FROM sales;
    '''
    
def Pip_Install():
    
    r64env = os.environ.copy()
    r64env["PYENV_ROOT"] = f"/home/row64/.pyenv"
    r64env["PATH"] = f"/home/row64/.pyenv/bin:{r64env['PATH']}"
    
    pipStr = """pip install row64tools
pip install pandas
pip install python-dotenv
pip install psycopg2
"""
    
    pipSPath = "/home/row64/r64tools/pipSetup.sh"
    f = open(pipSPath, "w")
    f.write(pipStr)
    f.close()
    os.chmod(os.path.join(pipSPath), 0o0777)
    sp.call(['bash', '-c',pipSPath], env=r64env)

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
PostgreSQL_Install()
Pip_Install()
Security_Setup()