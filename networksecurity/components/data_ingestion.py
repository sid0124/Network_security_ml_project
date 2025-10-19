from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant import training_pipeline

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo 
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd


from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self) : 
        try:
            data_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            collection = self.mongo_client[data_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            logging.info(f"Fetched {df.shape[0]} rows and {df.shape[1]} columns from MongoDB")

            if df.empty:
                raise NetworkSecurityException(
                    Exception(f"No data found in MongoDB collection: {data_name}.{collection_name}"), sys
                )

            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True, axis=1)
            df.replace({'na': pd.NA}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def split_data_as_train_test(self, dataframe:pd.DataFrame) :
          try:
                train_set, test_set = train_test_split(
                    dataframe, 
                    test_size=training_pipeline.DATA_INGESTION_TRIAN_TEST_SPLIT_RATION, 
                    random_state=42
                )
                logging.info("Performed train test split")

                logging.info("Exporting train and test file")

                dir_path= os.path.dirname(self.data_ingestion_config.train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Exporting train file path : {self.data_ingestion_config.train_file_path}")

                train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
                test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
                logging.info(f"Exporting test file path : {self.data_ingestion_config.test_file_path}")

          except Exception as e:
              raise NetworkSecurityException(e, sys)
   

    def export_data_into_feature_store(self,dataframe:pd.DataFrame) :
        """
        Export MongoDB collection as a pandas DataFrame.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_name = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_name, exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
        
    def initiate_data_ingestion(self) :
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
