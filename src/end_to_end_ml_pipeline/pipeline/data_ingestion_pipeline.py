from src.end_to_end_ml_pipeline.config.configuration import ConfigurationManager
from src.end_to_end_ml_pipeline.components.data_ingestion import DataIngestion   

from src.end_to_end_ml_pipeline import logger
STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        pass
      
    def initiate_data_ingestion(self):
        self.config = ConfigurationManager()
        data_ingestion_config = self.config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()


    