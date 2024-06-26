import logging
import os
from datetime import datetime

log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), "logs")

os.makedirs(log_path, exist_ok = True)

log_filepath = os.path.join(log_path, log_file)

logging.basicConfig(level = logging.INFO, 
        filename = log_filepath,
        format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)
