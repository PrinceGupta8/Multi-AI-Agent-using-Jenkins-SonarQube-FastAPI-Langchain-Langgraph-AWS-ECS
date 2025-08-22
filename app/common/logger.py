import logging
from datetime import datetime
import os
log_dir="logs"
os.makedirs(log_dir,exist_ok=True)
log_file=os.path.join(log_dir,f"logs_{datetime.now().strftime("%Y-%m-%d")}.log")

logging.basicConfig(filename=log_file,format=f"%(asctime)s -%(levelname)s - %(message)s")

def get_logger(name):
    logger=logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    return logger
