import pandas as pd
import os
from sklearn.linear_model import ElasticNet
from src.end_to_end_ml_pipeline.entity.config_entity import ModelTrainerConfig
from src.end_to_end_ml_pipeline.utils.common import save_bin, load_bin
from src.end_to_end_ml_pipeline import logger
import joblib
from pathlib import Path


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        """
        Initialize the ModelTrainer with the given configuration.

        Args:
            config: ModelTrainerConfig object containing configuration parameters.
        """
        self.config = config

    def train_model(self):
        """
        Train the ElasticNet model using the training data and save the trained model.
        """
        logger.info("Loading training data from: %s", self.config.train_data_path)
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        train_X = train_data.drop(columns=[self.config.target_column], axis=1)
        test_X = test_data.drop(columns=[self.config.target_column], axis=1)
        train_y = train_data[self.config.target_column]
        test_y = test_data[self.config.target_column]

        lr = ElasticNet(alpha=self.config.alpha, l1_ratio=self.config.l1_ratio, random_state=42)
        lr.fit(train_X, train_y)

        joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))
        logger.info("Model trained and saved at %s", os.path.join(self.config.root_dir, self.config.model_name))

