import os
import sys
import logging

# 1. Define a log format
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"

# 2. Make sure logs/ exists
log_dir = "logs"
log_file_path = os.path.join(log_dir, "logging_file.log")
os.makedirs(log_dir, exist_ok=True)

# 3. Configure root logging once
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout),
    ],
)

# 4. Create a named logger for this package
logger = logging.getLogger("end_to_end_ml_pipeline")
logger.setLevel(logging.INFO)

# 5. Expose `logger` so other modules can import it
__all__ = ["logger"]
