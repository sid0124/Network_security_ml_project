import os
from networksecurity.constant import training_pipeline

class DataIngestionConfig:
    def __init__(self):
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME

        self.feature_store_file_path = os.path.join(
            training_pipeline.ARTIFACT_DIR,
            training_pipeline.DATA_INGESTION_DIR_NAME,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        self.train_file_path = os.path.join(
            training_pipeline.ARTIFACT_DIR,
            training_pipeline.DATA_INGESTION_DIR_NAME,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.test_file_path = os.path.join(
            training_pipeline.ARTIFACT_DIR,
            training_pipeline.DATA_INGESTION_DIR_NAME,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )
