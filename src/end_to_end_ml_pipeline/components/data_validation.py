import os
import urllib.request as request
from src.end_to_end_ml_pipeline import logger
import zipfile
import pandas as pd
from src.end_to_end_ml_pipeline.entity.config_entity import (DataValidationConfig)

class DataValidation:

    def __init__(self, config: DataValidationConfig):
        """
        Initialize DataValidation with configuration.

        Args:
            config: DataValidationConfig object containing paths and thresholds.
        """
        self.config = config

    def validate_all_columns(self)-> bool:
        """
        Validate that all required columns are present in the dataset.

        Returns:
            bool: True if all required columns are present, False otherwise.
        """
        try:
            data_file_path = self.config.unzip_data_dir

            # Load the dataset
            data = pd.read_csv(data_file_path)
            all_colls = list(data.columns)  # Assuming 'data' is defined elsewhere with required columns

            all_schema = self.config.all_schema.keys()

            for col in all_colls:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation Status: {validation_status}\n")

                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation Status: {validation_status}\n")  


            return validation_status
        
        except Exception as e:
            raise e
        


      