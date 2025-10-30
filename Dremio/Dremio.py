import pandas as pd
import os
import sys
import pyarrow as pa

from row64tools import ramdb
from dotenv import load_dotenv
from http.cookies import SimpleCookie
from pyarrow import flight
from pyarrow import Table


def Dremio(inTablename):
	
	# Help page, https://docs.dremio.com/24.3.x/reference/sql/commands/

	class DremioClientAuthMiddlewareFactory(flight.ClientMiddlewareFactory):
		"""A factory that creates DremioClientAuthMiddleware(s)."""

		def __init__(self):
			self.call_credential = []

		def start_call(self, info):
			return DremioClientAuthMiddleware(self)

		def set_call_credential(self, call_credential):
			self.call_credential = call_credential

	class DremioClientAuthMiddleware(flight.ClientMiddleware):
		"""
		A ClientMiddleware that extracts the bearer token from
		the authorization header returned by the Dremio Cloud
		Flight Server Endpoint.

		Parameters
		----------
		factory : ClientHeaderAuthMiddlewareFactory
			The factory to set call credentials if an
			authorization header with bearer token is
			returned by Dremio Cloud.
		"""

		def __init__(self, factory):
			self.factory = factory

		def received_headers(self, headers):
			auth_header_key = 'authorization'
			authorization_header = []
			for key in headers:
				if key.lower() == auth_header_key:
					authorization_header = headers.get(auth_header_key)
			if not authorization_header:
				raise Exception('Did not receive authorization header back from server.')
			self.factory.set_call_credential([
				b'authorization', authorization_header[0].encode('utf-8')])

	class CookieMiddlewareFactory(flight.ClientMiddlewareFactory):
		"""A factory that creates CookieMiddleware(s)."""

		def __init__(self):
			self.cookies = {}

		def start_call(self, info):
			return CookieMiddleware(self)


	class CookieMiddleware(flight.ClientMiddleware):
		"""
		A ClientMiddleware that receives and retransmits cookies.
		For simplicity, this does not auto-expire cookies.

		Parameters
		----------
		factory : CookieMiddlewareFactory
			The factory containing the currently cached cookies.
		"""

		def __init__(self, factory):
			self.factory = factory

		def received_headers(self, headers):
			for key in headers:
				if key.lower() == 'set-cookie':
					cookie = SimpleCookie()
					for item in headers.get(key):
						cookie.load(item)

					self.factory.cookies.update(cookie.items())

		def sending_headers(self):
			if self.factory.cookies:
				cookie_string = '; '.join("{!s}={!s}".format(key, val.value) for (key, val) in self.factory.cookies.items())
				return {b'cookie': cookie_string.encode('utf-8')}
			return {}

	# Dremio Cloud connection via PAT
	# TLS Encryption is enabled. Certificate verification is disabled.
	headers = []
	connection_args = {}

	load_dotenv()
	
	# Construct middleware.
	client_cookie_middleware = CookieMiddlewareFactory()

	# Disable server verification
	connection_args['disable_server_verification'] = True

	# Establish initial connection
	client = flight.FlightClient("grpc+tls://data.dremio.cloud:443", middleware=[client_cookie_middleware], **connection_args)

	# Retrieve bearer token and append to the header for future calls.
	headers.append((b'authorization', "Bearer {}".format(os.environ["DBPAT"]).encode('utf-8')))
	
	query = 'SELECT * FROM ' + inTablename

	# Construct FlightDescriptor for the query result set.
	flight_desc = flight.FlightDescriptor.for_command(query)

	# Retrieve the schema of the result set.
	options = flight.FlightCallOptions(headers=headers)
	schema = client.get_schema(flight_desc, options)

	# Get the FlightInfo message to retrieve the Ticket corresponding
	# to the query result set.
	flight_info = client.get_flight_info(flight.FlightDescriptor.for_command(query), options)

	# Retrieve the result set as a stream of Arrow record batches.
	reader = client.do_get(flight_info.endpoints[0].ticket, options)
	
	df = reader.read_pandas()
	
	# example showing setting a column to datetime
	# df["date column"] = pd.to_datetime(df["date column"])
	
	# more details on saving to .ramdb: https://pypi.org/project/row64tools/
	ramdb.save_from_df(df, "/var/www/ramdb/live/RAMDB.Row64/Temp/Test.ramdb")
	

tableName = "myTable"
Dremio(myTable)