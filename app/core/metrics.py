import threading
import json
import logging
from pathlib import Path
from datetime import datetime
from .config import settings

logger = logging.getLogger(__name__)

class MetricsManager:
    def __init__(self, persistence_path: Path):
        self.path = persistence_path
        self.lock = threading.Lock()
        self.data = {
            "total_uploads": 0,
            "total_downloads": 0,
            "total_requests": 0,
            "start_time": datetime.utcnow().isoformat(),
            "errors": 0
        }
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    self.data.update(json.load(f))
            except Exception as e:
                logger.error(f"Failed to load metrics from {self.path}: {e}")

    def _save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics to {self.path}: {e}")

    def record_upload(self):
        with self.lock:
            self.data["total_uploads"] += 1
            self.data["total_requests"] += 1
            self._save()

    def record_download(self):
        with self.lock:
            self.data["total_downloads"] += 1
            self.data["total_requests"] += 1
            self._save()

    def record_error(self):
        with self.lock:
            self.data["errors"] += 1
            self.data["total_requests"] += 1
            self._save()

    def record_request(self):
        with self.lock:
            self.data["total_requests"] += 1
            self._save()

    def get_stats(self):
        with self.lock:
            return self.data.copy()

metrics = MetricsManager(settings.BASE_DIR / "data" / "metrics.json")
