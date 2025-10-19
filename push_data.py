import os
import sys
import json
import pandas as pd
import pymongo
import certifi
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()
MONGO_DB_URI = os.getenv("MONGODB_URI")
ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def test_connection(self):
        """Test MongoDB Atlas connection"""
        try:
            client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            
        except Exception as e:
            raise NetworkSecurityException(f"MongoDB Connection Failed: {e}", sys)

    def cv_to_json_convertor(self, file_path):
        """Convert CSV data into JSON records"""
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongoDB(self, records, database, collection):
        """Insert records into MongoDB collection"""
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "Sidharth"
    COLLECTION = "NetworkSecurity"

    networkobj = NetworkDataExtract()

    
    networkobj.test_connection()

   
    records = networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(f"📄 Total records extracted: {len(records)}")

    no_of_records = networkobj.insert_data_mongoDB(records, DATABASE, COLLECTION)
    print(f"🚀 Successfully inserted {no_of_records} records into MongoDB.")
