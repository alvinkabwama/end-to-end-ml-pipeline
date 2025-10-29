import os
from src.end_to_end_ml_pipeline import logger
from sklearn.model_selection import train_test_split
from src.end_to_end_ml_pipeline.entity.config_entity import DataTransformationConfig

import pandas as pd


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config   

        ## You can have different transformation techniques here like Scaler, Encoder etc.

    def train_test_splitting(self):
        data = pd.read_csv(self.config.data_path)

        #Splitting the data into train test_split

        train, test = train_test_split(data, test_size=0.2, random_state=42)

        train.to_csv(os.path.join(self.config.root_dir, 'train.csv'), index=False)
        test.to_csv(os.path.join(self.config.root_dir, 'test.csv'), index=False)

        logger.info("Train-test split completed successfully")
        logger.info(f"Train data shape: {train.shape}")
        logger.info(f"Test data shape: {test.shape}")
