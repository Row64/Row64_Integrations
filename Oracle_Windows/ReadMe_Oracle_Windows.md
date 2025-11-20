# Oracle Windows Integration
<img src="../Images_Oracle_Windows/Oracle_Row64_Windows_Integration.png" width="700">
<br>

Oracle is considered to be the most popular enterprise database. It has been available on Windows since 1994, and all of the most powerful and popular Oracle Database features are present on Windows. Oracle for Windows offers the benefit of operating Oracle in a familiar environment, and is fast to deploy for Windows IT experts.

!!! note
    This page is dedicated to the Windows integration. For the Linux integration, please see the [Oracle](Oracle.md) page.

## Integration Overview

This Oracle Database integration is established in Windows, and for data visualization, it transfers a .ramdb file to Ubuntu to serve dashboards. This strategy simplifies security and administration for Oracle Server professionals.

<img src="../Images_Oracle_Windows/Oracle_Row64_Win_Process.png" width="650">
<br>

The basic connection process involves using row64tools to push updates from an Oracle Database to Row64. An overview is available here:<br>
[https://pypi.org/project/row64tools/](https://pypi.org/project/row64tools/)

An overview of securely transferring files using SCP in Python is described here:<br>
[https://www.tutorialspoint.com/how-to-copy-a-file-to-a-remote-server-in-python-using-scp-or-ssh](https://www.tutorialspoint.com/how-to-copy-a-file-to-a-remote-server-in-python-using-scp-or-ssh)


## Minimal Test Setup

This tutorial shows how to complete a quick test with the Oracle Database XE version. This version is for development tests and non-commercial work. It's expected you'll switch to the commercial Oracle Database Enterprise Edition once your test is working.  

## Install Oracle Linux For Windows

!!! note
    Make sure you are logged into Windows as a user with administrative privileges.

If any of the following Oracle environment variables are set, delete them:

 - ORACLE_HOME

 - TNS_ADMIN

Download the current version of Oracle Database Express Edition for Windows:<br>
[https://www.oracle.com/database/technologies/xe-downloads.html](https://www.oracle.com/database/technologies/xe-downloads.html)


<img src="../Images_Oracle_Windows/Oracle_Windows_Dowload.png" width="500">
<br>

Right-click `OracleXE213_Win64.zip` and select "Extract All." Extract the files into a temporary location of your choosing.

In the extracted folder, double-click `setup.exe`.

Accept the default settings.  When you are prompted to create a database password, use: `temp7`


<img src="../Images_Oracle_Windows/Oracle_Win_Set_Pwd.png" width="500">

This is a simple test password to match the Python in this example

Continue to accept the default settings and complete the install.

<img src="../Images_Oracle_Windows/Oracle_Win_Install_Success.png" width="500">

When the installation completes, it will provide the information needed to connect to the default pluggable database.

!!! info
    If you experience issues with the installation, the following article provides an in-depth overview of the installation process. This article is from Oracle's official documentation site:<br>
    [https://docs.oracle.com/en/database/oracle/oracle-database/21/xeinw/installing-oracle-database-xe.html](https://docs.oracle.com/en/database/oracle/oracle-database/21/xeinw/installing-oracle-database-xe.html)


## Create a Pluggable Database User

It is not possible to connect to the database as SYSTEM to create the tables that are accessed from Python. This approach is insecure, so Oracle prevents it. Instead, you will first connect to the example pluggable database (XEPDB1) as `sys as sysdba`. From there, you will create a new user, `radmin`, which will be the account used to create and query tables from Python.

<img src="../Images_Oracle_Windows/Oracle_Wind_Pluggable_Database.png" width="700">
<br>

To get started, open the command prompt to begin creating a new default Pluggable Database (PDB). In the command prompt, type:

```
sqlplus sys/temp7@XE as sysdba
```

It should log you into an Oracle SQL command prompt:

<img src="../Images_Oracle_Windows/Oracle_Win_Prompt.png" width="600">
<br>

## Create an Oracle User

Next, create the C##radmin7 user to access from Python. This user should use the temporary password: `temp7`

!!! note
    This is a common user, so the name is prefixed with `C##`. A common user is a user that is known to the root and all pluggable databases. Using a common user will suffice for this test setup.

In the command prompt, type:

```
create user C##radmin7 identified by temp7;
```

Grant the privileges needed to log in and create tables. Note that we need to set ```container=all``` to have it work on pluggable databases:

```
grant create table to C##radmin7 container=all;
```

```
grant create session to C##radmin7 container=all; 
```

Next, grant privileges to insert data into tables:

```
alter user C##radmin7 quota unlimited on users container=all;
```

Finally, grant the full privileges needed to create views, procedures, and sequences. This is only for our example;
in production, you should only give users the least amount of privileges they need to operate.

```
grant create view, create procedure, create sequence to C##radmin7 container=all;
```

Exit the SQL Prompt so we can log in as a different user:

```
EXIT
```

If you have any trouble, more details on this process are found here:<br>
[https://blogs.oracle.com/sql/how-to-create-users-grant-them-privileges-and-remove-them-in-oracle-database](https://blogs.oracle.com/sql/how-to-create-users-grant-them-privileges-and-remove-them-in-oracle-database)

## Create Test Data

In the terminal, log in as the new C##radmin7 user:

```
sqlplus C##radmin7/temp7@//localhost:1521/XEPDB1
```

Create a new table with test data. Enter each line one at a time:

```
CREATE TABLE sales (tdate TIMESTAMP, amount DECIMAL(15,2), product VARCHAR2(50));
```

```
INSERT INTO sales (tdate,amount,product) VALUES (TIMESTAMP'2025-01-21 13:23:44', 446.57, 'Seal SE Robotic Pool Vacuum');
```

```
INSERT INTO sales (tdate,amount,product) VALUES (TIMESTAMP'2025-01-21 13:23:52', 287.24, 'Tikom Robot Vacuum and Mop');
```

```
INSERT INTO sales (tdate,amount,product) VALUES (TIMESTAMP'2025-01-21 13:24:03', 1376.28, 'ECOVACS DEEBOT T20 Omni Robot Vacuum');
```

```
INSERT INTO sales (tdate,amount,product) VALUES (TIMESTAMP'2025-01-21 13:24:17', 3200.10, 'Husqvarna Automower 430XH');
```

Query some sample data from the table:

```
SELECT tdate,amount,product FROM sales;
```

<img src="../Images_Oracle_Windows/Oracle_Win_Log_Data.png" width="650">

Exit the SQL Prompt:

```
EXIT
```



## Install Python on Windows 

To start, install the latest version of Python from:<br>
[https://www.python.org/downloads/](https://www.python.org/downloads/)

<img src="../Images_Oracle_Windows/Download_Python.png" width="500">

Downloading the Python install manager is an easy approach because it installs the environment variables to run Python from the command line.

Once it's installed, verify that the Python prompt is working in the command line. Open a command prompt and type:

```
python
```

You should see the Python prompt appear in the terminal. To exit the Python prompt, type:

```
quit
```

Next, set up the Python pip libraries needed for the integration. Type the following commands in the terminal, entering them one line at a time:

```
python -m pip install row64tools
```

```
python -m pip install python-dotenv
```

```
python -m pip install oracledb
```

```
python -m pip install paramiko
```

```
python -m pip install scp
```

## Set Up Login Credentials in .env

You will need to create a .env file from the command prompt and edit it in Notepad.

Use the following commands to create the .env file at the specified directory location. This directory can also be used to save .ramdb files.

```
mkdir C:\r64tools
cd C:\r64tools
.>db.env 2>NUL
notepad db.env
```

With the .env file open in Notepad, input the example setup data:

```
DBHost=localhost/xepdb1
DBUser=C##radmin7
DBPwd=temp7
SSH_Host=192.168.1.10
SSH_Port=22
SSH_User=row64
SSH_Pwd=temp7
```

You can update this configuration at a later point with the correct information for your particular setup. It is important to use SSH with the `row64` user, because files need to be transferred with an account that has access to row64server.

## Download Oracle Windows Integration

The Row64 integration for Oracle can be downloaded from:<br>
[https://github.com/Row64/Row64_Integrations/tree/master/Oracle](https://github.com/Row64/Row64_Integrations/tree/master/Oracle)

Download the integration and copy the `Oracle_Windows_RamDB.py` file into the folder location:

`C:\r64tools\Oracle_Windows_RamDB.py`

In the terminal, run the Python integration with the following commands:

```
cd C:\r64tools
python Oracle_Windows_RamDB.py
```

The terminal should print the example table and display the status of the transfer.

<img src="../Images_Oracle_Windows/Oracle_Win_Integration_Working.png" width="600">

## Verify File Transfer is Working 

When you ran `SQLServer_RamDB.py`, it attempted to transfer the new .ramdb file using SCP to the server specified in:

```
C:\r64tools\db.env
```

For this to work, it is important to verify that the file is set up correctly.

Additionally, on the Ubuntu machine you are copying to, make sure you've installed Row64 Server.

You will also need to make the loading folder that recieves your .ramdb file. For this minimal example, use the following command to create the needed folder at the specified location:

```
mkdir -p /var/www/ramdb/loading/RAMDB.Row64/Temp
```

Also, it's best to set the `SSH_User` field to `row64` so that when the copied file is received, the row64server service has access to it.

```
SSH_User=row64
```

## Set Up SSH on Ubuntu 

If you only completed the default Ubuntu installation, it's likely that SSH is not set up on your server or instance.

In Ubuntu, check the list of installed UFW profiles with:

```
sudo ufw app list
```

If OpenSSH is not listed, install it with:

```
sudo apt install openssh-server
```

Enable SSH connections and the firewall:

```
sudo ufw allow OpenSSH
sudo ufw enable
```

!!! note
    This integration routes a SSH login and password in the example .py file.  The setup can be modified for a higher tier of security using a SSH key, which is an access credential in the SSH protocol

## Debug Windows to Linux SSH

If you created the .ramdb file in `C:\r64tools\Test.ramdb ` but are not able to copy it over to Ubuntu, you can debug the port connections with ping and telnet. In the following commands, substitute the example IP addresses with your own hostnames or IPs:

Ping:
```
ping 192.168.1.10
```

Telnet:
```
telnet 192.168.1.10 22
```

For reference, the following article discusses resolving these issues:<br>
[https://stackoverflow.com/questions/14143198/errno-10060-a-connection-attempt-failed-because-the-connected-party-did-not-pro](https://stackoverflow.com/questions/14143198/errno-10060-a-connection-attempt-failed-because-the-connected-party-did-not-pro)

<!-- PAUSED HERE -->

## Test with ByteStream Viewer

Once you see the file copy over to Ubuntu, you can install ByteStream Viewer to visualize the data.

To install ByteStream Viewer on Ubuntu, you can reference the following documentation:<br>
[Install ByteStream Viewer on Ubuntu](../../V3_5/Install_Docs/Streaming/Stream_Install_Ubuntu.md/#install-bytestream-viewer)

You can drag the .ramdb file right into the ByteStream Viewer

<img src="../Images_Oracle_Windows/Oracle_Win_ByteStream.png" width="550">

<br>
Alternatively, you can simply open the file in Row64 Studio.

## Continuous Update

On Windows, Task Scheduler is the production-proven tool for establishing continuous updates.  Here's a simple example on how to set it up:<br>
[https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10)

<img src="../Images_Oracle_Windows/Oracle_Win_Task_Scheduler.png" width="600">

You simply need to take the integration .py file and set up a cron job to run at your data refresh rate, which can range from every 20 seconds to every day.






