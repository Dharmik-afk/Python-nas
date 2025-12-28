import sys
import logging
from pathlib import Path

# Ensure project root is in path to allow importing from scripts
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from scripts.manage import sync_users_to_copyparty
except ImportError:
    # Fallback or alternative import path if needed
    # (Sometimes 'scripts' is not a package, so we might need special handling)
    def sync_users_to_copyparty():
        logging.error("Could not import sync_users_to_copyparty from scripts.manage")
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sync_users_to_copyparty()