import pandas as pd
import sqlite3

from row64tools import ramdb
from dotenv import load_dotenv

def SQLite(inTableName, inSqlPath):
    
    # Help page, https://datacarpentry.github.io/python-ecology-lesson/instructor/09-working-with-sql.html

    conn = sqlite3.connect(inSqlPath)
    df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)
    
    # example showing setting a column to datetime
    # df["date column"] = pd.to_datetime(df["date column"])
    
    # more details on saving to .ramdb: https://pypi.org/project/row64tools/
    ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


tableName = "Customer"
sqlitePath = "demo.sqlite"
SQLite( tableName, sqlitePath)
