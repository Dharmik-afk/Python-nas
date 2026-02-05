import logging
from pathlib import Path

# Import from scripts using absolute import
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