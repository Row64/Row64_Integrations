import pandas as pd
import os
import snowflake.connector
import pyarrow as pa

from row64tools import ramdb
from dotenv import load_dotenv


def Snowflake(inTableName):
    
    # Please set the following environment variables: DBUser, DBPassword, DBAccount to proper values.
    load_dotenv()

    # Help page, https://docs.snowflake.com/en/sql-reference/constructs
    
	conn = snowflake.connector.connect(
        user=os.environ["DBUser"],
        password=os.environ["DBPassword"],
        account=os.environ["DBAccount"]
    )

    df = pd.read_sql_query("SELECT * FROM " + inTablename, conn)

    # example showing setting a column to datetime
    # df["date column"] = pd.to_datetime(df["date column"])
    
    # more details on saving to .ramdb: https://pypi.org/project/row64tools/
    ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")


tableName = "myTable"
Snowflake( tableName )
