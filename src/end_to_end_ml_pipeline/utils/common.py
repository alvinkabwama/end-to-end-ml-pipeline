import os
import yaml
from src.end_to_end_ml_pipeline import logger
import json
import pickle
import joblib
from typing import Any, Union
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from pathlib import Path


@ensure_annotations
def read_yaml(path_to_yaml: Union[str, Path]) -> ConfigBox:
    """Read a YAML file and return its contents as a ConfigBox.

    Why ConfigBox?
    - It lets you access keys like attributes (cfg.some_key) instead of cfg["some_key"].

    Args:
        path_to_yaml (str): Path to the YAML file.

    Returns:
        ConfigBox: Parsed YAML content wrapped in ConfigBox.

    Raises:
        ValueError: If the YAML is empty or invalid.
        Exception: For any other I/O or parsing error.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
        logger.info(f"YAML file loaded successfully: {path_to_yaml}")
        return ConfigBox(content)
    except BoxValueError:
        # BoxValueError usually means yaml.safe_load() returned None or invalid structure
        logger.error(f"YAML file is empty or invalid: {path_to_yaml}")
        raise ValueError(f"YAML file is empty or invalid: {path_to_yaml}")
    except Exception as e:
        logger.error(f"Error reading the YAML file {path_to_yaml}: {e}")
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose= True):
    """Create directories if they don't exist.
    Args:
        paths (list): List of directory paths to create.
        verbose (bool): If True, logs each created directory.
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose: 
            logger.info(f"Directory created/verified at: {path}")
    


def save_json(path: str, data: dict) -> None:
    """Save a dictionary to a JSON file.

    Args:
        path (str): Destination path for the JSON file.
        data (dict): The dictionary to serialize.

    Notes:
        indent=4 makes it human-readable.
    """
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    logger.info(f"JSON file saved at: {path}")



def load_json(path: str) -> ConfigBox:
    """Load a JSON file and return its content.

    Args:
        path (str): Path to the JSON file.

    Returns:
        ConfigBox: JSON content wrapped so you can use dot notation.
    """
    with open(path, "r") as json_file:
        data = json.load(json_file)
    logger.info(f"JSON file loaded from: {path}")
    return ConfigBox(data)



def save_bin(data: object, path: Union[Path, str]) -> None:
    """Serialize any Python object to disk using joblib.

    Common use:
    - Save trained ML models, scalers, vectorizers, etc.

    Args:
        data (Any): The object to persist (model, transformer, etc.).
        path (Path): Where to store the binary file, e.g. Path("artifacts/model.joblib").
    """
    joblib.dump(data, path)
    logger.info(f"Binary file (joblib) saved at: {path}")



def load_bin(path: Union[Path, str]) -> Any:
    """Load an object that was saved with joblib.dump().

    Args:
        path (Path): Path to the .joblib (or .bin) file.

    Returns:
        Any: The deserialized Python object (e.g. trained model).
    """
    obj = joblib.load(path)
    logger.info(f"Binary file (joblib) loaded from: {path}")
    return obj



def save_pickle(data: Any, path: Path) -> None:
    """Serialize any Python object to disk using pickle.

    Args:
        data (Any): The object to persist.
        path (Path): Where to store it, e.g. Path("artifacts/model.pkl").

    Notes:
        protocol=pickle.HIGHEST_PROTOCOL gives you best/most efficient binary format
        for your current Python version.
    """
    with open(path, "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    logger.info(f"Pickle file saved at: {path}")


def load_pickle(path: Path) -> Any:
    """Load an object that was saved with pickle.dump().

    Args:
        path (Path): Path to the .pkl file.

    Returns:
        Any: The restored Python object.
    """
    with open(path, "rb") as f:
        obj = pickle.load(f)
    logger.info(f"Pickle file loaded from: {path}")
    return obj
