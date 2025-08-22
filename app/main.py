import threading
import subprocess
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend services....")
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999", "--reload"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.exception(f"Problem with backend services: {e}")
        raise CustomException("Failed to start backend", e)

def run_frontend():
    try:
        logger.info("Starting frontend services....")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except subprocess.CalledProcessError as e:
        logger.exception(f"Problem with frontend services: {e}")
        raise CustomException("Failed to start frontend", e)
    
if __name__ == "__main__":
    try:
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        time.sleep(2)  # wait for backend to start
        run_frontend()
    except Exception as e:
        logger.exception(f"Error occurred in main: {e}")
