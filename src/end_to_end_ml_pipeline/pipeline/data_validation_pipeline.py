from src.end_to_end_ml_pipeline import logger
from src.end_to_end_ml_pipeline.components.data_validation import DataValidation
from src.end_to_end_ml_pipeline.config.configuration import ConfigurationManager

STAGE_NAME = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        self.config = ConfigurationManager()
        data_validation_config = self.config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.validate_all_columns()

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<")
        data_validation_pipeline = DataValidationPipeline()
        data_validation_pipeline.initiate_data_validation()
        logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e




