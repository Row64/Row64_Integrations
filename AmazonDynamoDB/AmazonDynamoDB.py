import pandas as pd
import os

from row64tools import ramdb
from dotenv import load_dotenv
import boto3

def AmazonDynamoDB():

	print("---------- Before Connect -----------")
	ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
	print("---------- Connect Success -----------")

	table = ddb.Table('Sales')
	response = table.scan()
	result = response['Items']
	while 'LastEvaluatedKey' in response:
		response=table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		result.extend(response['Items'])
	df = pd.DataFrame(result)
	
	df["date"] = pd.to_datetime(df["date"])
	print(df) # temporary, remove when using in production
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/loading/RAMDB.Row64/Temp/Test.ramdb")

AmazonDynamoDB()