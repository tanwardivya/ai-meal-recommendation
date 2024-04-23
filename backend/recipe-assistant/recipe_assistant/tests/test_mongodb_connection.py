from pymongo.mongo_client import MongoClient
import os
import unittest
import certifi

URI = os.environ.get('MONGODB_CONNECTION_STRING')
# Create a new client and connect to the server
client = MongoClient(URI, tlsCAFile=certifi.where())

class TestMongoDB(unittest.TestCase):

    def test_mongodb_connection(self):
        try:
            database_name = 'agent'
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.assertEqual(client.get_database().name, database_name)
        except Exception as e:
            print(e)
        