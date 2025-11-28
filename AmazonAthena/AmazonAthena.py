import pandas as pd
import os
import sys

from row64tools import ramdb
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from urllib.parse import quote_plus

def AmazonAthena( inTableName ):
	
	# Please set the following environment variables: DBAccKey, DBSecKey, DBRegion, DBSchema, and DBS3Dir
	load_dotenv()
	
	# Help page, https://medium.com/codex/connecting-to-aws-athena-databases-using-python-4a9194427638

	YOUR_ACCESS_KEY_ID = os.environ["DBAccKey"]
	YOUR_SECRET_ACCESS_KEY = os.environ["DBSecKey"]
	REGION_NAME = os.environ["DBRegion"]	# i.e., "us-west-2"
	SCHEMA_NAME = os.environ["DBSchema"]	# i.e., "default"
	S3_STAGING_DIR = os.environ["DBS3Dir"]	# i.e., "s3://YOUR_S3_BUCKET/path/to/"

	conn_str = "awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}"\
		"@athena.{region_name}.amazonaws.com:443/"\
        "{schema_name}?s3_staging_dir={s3_staging_dir}"

	engine = create_engine(
		conn_str.format(
			aws_access_key_id=quote_plus(YOUR_ACCESS_KEY_ID),
			aws_secret_access_key=quote_plus(YOUR_SECRET_ACCESS_KEY),
			region_name=REGION_NAME,
			schema_name=SCHEMA_NAME,
			s3_staging_dir=quote_plus(S3_STAGING_DIR),
		)
	)

	try:
		conn = engine.connect()
	except engine.Error as e:
		print(f"Error connecting to database: {e}")
		sys.exit(1)

	df = pd.read_sql_query("SELECT * FROM " + inTableName, conn)

	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])

	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")

tableName = "TableName"
AmazonAthena( tableName )