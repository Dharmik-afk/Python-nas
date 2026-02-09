import subprocess
import time
import signal
import sys
import logging
import urllib.request
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
# Import app modules using absolute imports
from app.core.config import settings
from app.core.utils import generate_opener_script

# Configure logging for Supervisor
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Supervisor] %(message)s")
logger = logging.getLogger(__name__)

VENV_PYTHON = sys.executable
COPYPARTY_CONF = BASE_DIR / "copyparty" / "copyparty.conf"

# Process handles
copyparty_proc = None
uvicorn_proc = None

def start_copyparty():
    global copyparty_proc
    # Bind Copyparty to the configured host (e.g., 0.0.0.0 for UI access)
    cmd = [
        VENV_PYTHON, "-m", "copyparty",
        "-c", str(COPYPARTY_CONF),
        "-i", settings.COPYPARTY_HOST,
        "-p", str(settings.COPYPARTY_PORT)
    ]
    
    logger.info(f"Starting Copyparty: {' '.join(cmd)}")
    copyparty_proc = subprocess.Popen(cmd)

def start_uvicorn():
    global uvicorn_proc
    cmd = [
        VENV_PYTHON, "-m", "uvicorn",
        "app.main:app",
        "--host", settings.FRONTEND_HOST,
        "--port", str(settings.FRONTEND_PORT)
    ]
    logger.info(f"Starting Uvicorn: {' '.join(cmd)}")
    uvicorn_proc = subprocess.Popen(cmd)

def check_health():
    try:
        # Use the configured host for health check
        health_url = f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}/health"
        with urllib.request.urlopen(health_url, timeout=2) as response:
            if response.status == 200:
                return True
    except Exception:
        pass
    return False

def shutdown(signum, frame):
    logger.info("Shutdown signal received. Terminating processes...")
    
    # Terminate FastAPI first to close active proxy connections
    if uvicorn_proc:
        logger.info("Terminating Uvicorn...")
        uvicorn_proc.terminate()
    
    # Wait a moment for Uvicorn to release sockets
    if copyparty_proc:
        time.sleep(1)
        logger.info("Terminating Copyparty...")
        copyparty_proc.terminate()

    # Wait for both to exit
    if uvicorn_proc:
        uvicorn_proc.wait(timeout=5)
    if copyparty_proc:
        copyparty_proc.wait(timeout=5)
        
    logger.info("All processes terminated. Exit.")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Generate the opener script
    try:
        generate_opener_script(settings.FRONTEND_PORT, settings.FRONTEND_HOST)
    except Exception as e:
        logger.error(f"Failed to generate opener script: {e}")

    start_copyparty()
    time.sleep(2) # Give copyparty a moment to initialize
    start_uvicorn()

    # Allow Uvicorn to start
    time.sleep(5)

    while True:
        if copyparty_proc.poll() is not None:
            logger.error("Copyparty exited unexpectedly! Restarting...")
            start_copyparty()
        
        if uvicorn_proc.poll() is not None:
            logger.error("Uvicorn exited unexpectedly! Restarting...")
            start_uvicorn()
        
        if not check_health():
             logger.warning("FastAPI health check failed!")
             # Optional: Restart logic based on health check failure count could go here
        
        time.sleep(10)

if __name__ == "__main__":
    main()