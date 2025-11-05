import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from pymongo import MongoClient

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    
    return conn[db]


def MongoDB(inDb, inTablename):

	# Please set the following environment variables: DBHost, DBUsername, DBPort, DBPwd to proper values.
	load_dotenv()
	
	# Help page, https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/

	db = _connect_mongo(host=os.environ["DBHost"], port=os.environ["DBPort"], username=os.environ["DBUsername"], password=environ["DBPwd"], db=inDb)

	# df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

	query={}
	cursor = db[collection].find(query)
	df = pd.DataFrame(list(cursor))
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")

db = "Examples"
tableName = "myTable"
MongoDB( db. tableName)