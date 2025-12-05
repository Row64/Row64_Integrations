# Apache Parquet File Integration

<img src="images/Parquet_Integration.png" width="500">

Apache Parquet is an open-source data file format for columnar data. Parquet is an industry standard, and is widely used in cloud data warehouses and data lakes. It is also supported by many programming languages. Apache Parquet integrates easily with Row64 by wiring to Row64 RamDb through Python.


## Integration Overview

This integration primarily uses Python Pandas. This walkthrough will guide you in establishing an integration with Parquet, which will involve:

* Running the integration in Ubuntu 25.01

* Creating and transferring `.parquet` files to Row64 Server

* Converting the `.parquet` files to `.ramdb` files

* Loading the updates to dashboards


## Download the Integration

Download the Row64 integration for Parquet from GitHub:

* [https://github.com/Row64/Row64_Integrations/tree/master/Parquet](https://github.com/Row64/Row64_Integrations/tree/master/Parquet)


## Set Up a Non-OS Python

For working with Python in Ubuntu, when you need to perform pip installations, it's best practice to install a second instance of Python. This will prevent pip dependencies from corrupting Ubuntu system calls.

The simplest way to accomplish this is to install `pyenv`. For further reading, the following article explains managing multiple instances of Python with `pyenv`:

* [https://realpython.com/intro-to-pyenv/](https://realpython.com/intro-to-pyenv/)

To simplify the setup, we've automated the `pyenv` installation.  From the root of the integration in [GitHub](https://github.com/Row64/Row64_Integrations/tree/master), download the `Setup_pyenv.py` and run it with:

```
python3 Setup_pyenv.py
```

Once `pyenv` is set up, you can work with the folder specific to the integration to install the needed pip libraries and Python integration, calling `python` instead of the OS-level `python3`. To do this, proceed to the next section.


## Install Python Pip Libraries

Install the Python libraries needed to connect to the database and transfer a `.ramdb` file. In a terminal, enter the following commands, one at a time:


```
pip install row64tools
```

```
pip install pyarrow
```


## Run the Integration

In a previous step, you should have downloaded the Python integration from GitHub. Now that the needed Python libraries are installed, you can run the integration. Use the following command:

```
python Parquet_To_Ramdb.py
```

If everything worked correctly, your terminal should output some lines of sample data:

<img src="images/Parquet_Python.png" width="650">


## Test with ByteStream Viewer

Once the file is successfully copying over to Ubuntu, you can use ByteStream Viewer to visualize the data.

To install ByteStream Viewer on Ubuntu, you can reference the following documentation. After installing and testing ByteStream Viewer, return to this page.

* [Install ByteStream Viewer on Ubuntu](../../V3_5/Install_Docs/Streaming/Stream_Install_Ubuntu.md/#install-bytestream-viewer)

You can drag and drop the `.ramdb` file into ByteStream Viewer to open it quickly.

<img src="images/Parquet_ByteStream.png" width="550">


## Set Up a Loading Folder

The final step is to create a loading folder and to transfer the `.ramdb` file to it. The loading folder acts as a drop folder where the server will retrive the file and update all future dashboards.

Creating a live loading folder involves *row64tools*. For further reading, more information on row64tools is available at the following article. Please note that you already installed row64tools in a previous step, so there is no need to install it again.

* [https://pypi.org/project/row64tools/](https://pypi.org/project/row64tools/)

Create a directory for loading. Create this folder as the `row64` user so that Row64 has proper access to it:

```
mkdir -R /var/www/ramdb/loading/RAMDB.Row64/Temp
```

Next, modify the integration .py file so that you write into the new loading folder. Open the integration .py file in a text editor and locate the following line:

```
ramdbPath = 'test.ramdb'
```

Change the value of `ramdbPath` to:

```
ramdbPath = '/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb'
```

Save the file. Now, it will automatically push updates to Row64 Server. From here, you can modify the name of the folder and the `.ramdb` file to load different dataframes into different folders, if desired.


