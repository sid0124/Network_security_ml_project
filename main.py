from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
import sys

if __name__=="__main__":
    try:
        logging.info("NetworkSecurity")
        data_ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"artifact {data_ingestion_artifact}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
