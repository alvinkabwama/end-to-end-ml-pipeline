import os
import urllib.request
import zipfile
from pathlib import Path
from src.end_to_end_ml_pipeline import logger
from src.end_to_end_ml_pipeline.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """
        Initialize DataIngestion with configuration.

        Args:
            config: DataIngestionConfig object containing paths and URLs.
        """
        self.config = config

    def download_file(self) -> None:
        """
        Download the data file from the source URL to the local data file path. 
        """

        if not os.path.exists(self.config.local_data_file):
            filename, headers = urllib.request.urlretrieve(
                url = self.config.source_URL, 
                filename = self.config.local_data_file
            )
            logger.info(f"File downloaded successfully into {filename}")

        else:
            logger.info(f"File already exists at {self.config.local_data_file}. Skipping download.")

    def extract_zip_file(self) -> None:
        """
        Extract the downloaded zip file into the specified unzip directory.
        """
        unzip_dir   = self.config.unzip_dir
        os.makedirs(unzip_dir, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(self.config.unzip_dir)
            logger.info(f"File extracted successfully into {self.config.unzip_dir}")


