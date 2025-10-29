from src.end_to_end_ml_pipeline.config.configuration import ConfigurationManager
from src.end_to_end_ml_pipeline.components.data_transformation import DataTransformation
from src.end_to_end_ml_pipeline import logger
from pathlib import Path


STAGE_NAME = "Data Transformation Stage"  

class TransformationPipeline():
    def __init__(self):
        pass

    def _read_validation_status(self, path: Path) -> bool:
        """
        Read 'Validation Status: <True|False>' and return a boolean.
        Accepts variations in whitespace/case and trailing newline.
        """
        text = path.read_text(encoding="utf-8").strip()
        # Try to split on colon first; fallback to last token if colon missing
        if ":" in text:
            value = text.split(":", 1)[1].strip()
        else:
            value = text.split()[-1].strip()
        return value.lower() in {"true", "1", "yes"}

    def initiate_data_transformation(self):
        try:
            status_path = Path("artifacts/data_validation/status.txt")
            is_valid = self._read_validation_status(status_path)
            
            if is_valid == True:
                config = ConfigurationManager()
                data_trransformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_trransformation_config)
                data_transformation.train_test_splitting()

            else:
                raise Exception("Data Validation not completed. Cannot proceed to Data Transformation.")
            
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {e}")
            raise e 