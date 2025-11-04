# Row64 Integrations

Row64 is designed to easily connect to many Database, Data Lake and Data Application platforms.  

This project contains a folder per integration.  The primary strategy used is to pull from the data source and copy it into RamDb.  A general overview of this connection strategy is here:
https://pypi.org/project/row64tools/

The integrations are examples that are intended to be modified to fit your specific needs.  Linux distributions, Python, Pandas, connectors and security requirments are in a time period of rapid change.  So if you find any problems please log them under Issues and contact our support team if you are under a commercial license.

For high speed data streaming (where the update rate is in seconds or milliseconds) please check out Row64 streaming. There are a different set of connectors and a different connection strategy that pushes updates directly through the server to connected clients.  More details here:
https://app.row64.com/Help/V3_5/Install_Docs/Streaming/

These examples are mostly in Python but we intend to grow them in multiple languages.  We also intend to add some C++ low-level examples for higher speed at larger scales (10M-1B records).  For a dataset under 10 million records that is not frequently updating, Python should be sufficent.


 ## Python Integrations in Ubuntu 

Since Ubuntu 24.04 and forward, you can't pip install on the OS level python.
This is to prevent interfering with the OS python calls and corrupt the OS 
 
The solution is to install a second version of python, and then pip install
to that new version.  The simplest way to do this is to install pyenv
More details here: https://realpython.com/intro-to-pyenv/

To simplify setup, we've automated pyenv installation.  Run Setup_pyenv.py with:
```
python3 Setup_pyenv.py
```
After pyenv is setup, then you can work with the integration specific folder to install the needed pip libraries and python integration, calling 'python' instead of the OS-level 'python3'

<br>
<img src="Integrations.png" width="700">
<br>
