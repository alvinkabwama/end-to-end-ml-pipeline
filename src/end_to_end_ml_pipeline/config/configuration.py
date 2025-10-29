from pathlib import Path  # Needed for converting string paths into Path objects

# Import constants like CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
# These are probably defined somewhere like src/end_to_end_ml_pipeline/constants/__init__.py
from src.end_to_end_ml_pipeline.constants import *

# Import helper utilities:
# - read_yaml: loads YAML into a ConfigBox (so you can do .field instead of ["field"])
# - create_directories: ensures folders exist
from src.end_to_end_ml_pipeline.utils.common import read_yaml, create_directories

# Import the dataclass (or pydantic model) that represents the config
# for the "data ingestion" stage of the pipeline.
from src.end_to_end_ml_pipeline.entity.config_entity import (DataIngestionConfig, DataValidationConfig
                                                             , DataTransformationConfig)

class ConfigurationManager:
    """
    Central config manager for the pipeline.

    This class:
    - Reads all the config files (.yaml) once
    - Creates required directories
    - Exposes typed config objects for each pipeline component (like data ingestion)

    Why this helps:
    - You don't hardcode paths all over the codebase.
    - Each pipeline stage gets a clean config object with just what it needs.
    """

    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH,
        schema_filepath=SCHEMA_FILE_PATH,
    ):
        """
        Initialize the ConfigurationManager.

        Args:
            config_filepath: path to the main config YAML (e.g. 'config/config.yaml')
            params_filepath: path to model/training parameters YAML (e.g. 'params.yaml')
            schema_filepath: path to schema YAML (e.g. 'schema.yaml' that defines columns)

        Behavior:
        - Reads YAML files into self.config / self.params / self.schema
        - Creates the root artifacts directory defined in config
        """

        # Load the main config file (usually has run directories, component configs, etc.)
        # This returns a ConfigBox, so you can access values with dot notation, e.g. self.config.data_ingestion.root_dir
        self.config = read_yaml(config_filepath)

        # Load params (hyperparameters, training settings, etc.)
        self.params = read_yaml(params_filepath)

        # Load schema (expected columns, dtypes, validation rules, etc.)
        self.schema = read_yaml(schema_filepath)

        # Make sure the root artifacts directory exists.
        # self.config.artifacts_root should come from the YAML.
        # This is something like: "artifacts/" or "artifacts/data_ingestion/"
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Build and return the DataIngestionConfig object.

        This isolates ONLY the settings that the data ingestion component cares about,
        instead of dumping the entire big config object on that component.

        Returns:
            DataIngestionConfig: an object that contains all config values
                                 needed by the data ingestion pipeline step.
        """

        # Pull just the `data_ingestion` section from the loaded config.
        # Example (from YAML):
        # data_ingestion:
        #   root_dir: artifacts/data_ingestion
        #   source_URL: "https://example.com/data.zip"
        #   local_data_file: artifacts/data_ingestion/data.zip
        #   unzip_dir: artifacts/data_ingestion/extracted
        #
        # After read_yaml(), you can access this with dot notation.
        config = self.config.data_ingestion

        # Make sure the data ingestion directory exists before we try to download/unzip into it.
        create_directories([config.root_dir])

        # Now build a strongly-typed config object for data ingestion.
        # We wrap file system paths in Path(...) (from pathlib) instead of leaving them as raw strings.
        # This gives us safer path handling and nicer APIs (like .exists(), .mkdir(), etc.).
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_URL=config.source_URL,
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir),
        )

        # Return that object so the data ingestion pipeline step can use it.
        # Example usage downstream:
        #   cfg = config_manager.get_data_ingestion_config()
        #   downloader = DataIngestion(cfg)
        #   downloader.download_zip()
        return data_ingestion_config
    

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Build and return the DataValidationConfig for the data-validation stage.

        Inputs:
            - (implicit) self.config: a config object loaded from YAML, expected to contain:
                - self.config.data_validation.root_dir: str | Path
                - self.config.data_validation.STATUS_FILE: str | Path
                - self.config.data_validation.unzip_dir: str | Path
            - (implicit) self.schema: a schema object loaded from YAML, expected to contain:
                - self.schema.COLUMNS: dict-like schema of expected columns/dtypes

        Process:
            - Reads the `data_validation` section from the main config.
            - Ensures the validation root directory exists.
            - Packs the paths and schema into a strongly-typed DataValidationConfig.

        Outputs:
            - Returns: DataValidationConfig
            A configuration record with:
                - root_dir: Path
                - STATUS_FILE: Path
                - unzip_data_dir: Path
                - all_schema: dict (columns spec)

        Side effects:
            - Creates the directory at `root_dir` if it does not already exist.

        Raises:
            - Any exceptions bubbled up from directory creation or attribute access
            if the config/schema are missing required fields.
        """
        # Pull the `data_validation` section and the column schema
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        # Normalize to Path for safer downstream usage
        root_dir = Path(config.root_dir)
        status_file = Path(config.STATUS_FILE)
        unzip_data_dir = Path(config.unzip_data_dir)

        # Ensure the validation directory exists before writing status files, etc.
        create_directories([root_dir])

        # Build and return the typed config object for the validation component
        data_validation_config = DataValidationConfig(
            root_dir=root_dir,
            STATUS_FILE=status_file,
            unzip_data_dir=unzip_data_dir,
            all_schema=schema,
        )
        return data_validation_config
    

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Build and return the DataTransformationConfig for the data-transformation stage.
        # Pull the `data_transformation` section from the main config.

        Inputs:
            - (implicit) self.config: a config object loaded from YAML, expected to contain:
                - self.config.data_transformation.root_dir: str | Path
                - self.config.data_transformation.transformed_data_dir: str | Path

        Process:
            - Reads the `data_transformation` section from the main config.
            - Ensures the transformation root directory exists.       
        Outputs:
            - Returns: DataTransformationConfig
            A configuration record with:
                - root_dir: Path
                - transformed_data_dir: Path
        Side effects:
            - Creates the directory at `root_dir` if it does not already exist.
        Raises:
            - Any exceptions bubbled up from directory creation or attribute access
            if the config are missing required fields.
        """
        config = self.config.data_transformation

        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path= config.data_path,
        )
        return data_transformation_config
