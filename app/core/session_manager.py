import logging
import uuid
import time
import threading
from collections import OrderedDict
from typing import Optional, List, Dict
import json
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)

class Session:
    """
    Represents a single user session.
    """
    def __init__(self, ip_address: str, user_agent: str):
        self.session_id: str = str(uuid.uuid4())
        self.ip_address: str = ip_address
        self.user_agent: str = user_agent
        self.start_time: float = time.time()
        self.last_seen: float = self.start_time
        self.activity: List[str] = []
        self._auth_header: Optional[str] = None # Encrypted Basic Auth string
        self._username: Optional[str] = None
        self.modified: bool = False

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if self._username != value:
            self._username = value
            self.modified = True

    @property
    def auth_header(self):
        return self._auth_header

    @auth_header.setter
    def auth_header(self, value):
        if self._auth_header != value:
            self._auth_header = value
            self.modified = True

    def touch(self):
        self.last_seen = time.time()

    def log_activity(self, message: str):
        self.touch()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        self.activity.append(f"[{timestamp} UTC] {message}")
        if len(self.activity) > 10:
            self.activity.pop(0)
        self.modified = True

    def to_dict(self) -> dict:
        return {
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'start_time': self.start_time,
            'last_seen': self.last_seen,
            'activity': self.activity,
            'auth_header': self.auth_header,
            'username': self.username,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Session':
        session = cls(data['ip_address'], data['user_agent'])
        session.session_id = data['session_id']
        session.start_time = data['start_time']
        session.last_seen = data['last_seen']
        session.activity = data['activity']
        session._auth_header = data.get('auth_header')
        session._username = data.get('username')
        session.modified = False
        return session

class SessionManager:
    """
    Manages active user sessions with persistence and thread safety.
    """
    def __init__(self, save_path: Path):
        self._sessions: OrderedDict[str, Session] = OrderedDict()
        self.max_sessions = settings.SESSION_MAX_COUNT
        self.timeout_seconds = settings.SESSION_TIMEOUT_SECONDS
        self._save_path = save_path
        self._lock = threading.Lock()
        self.load_sessions()

    def load_sessions(self):
        if not self._save_path.exists():
            return
        
        try:
            with open(self._save_path, 'r') as f:
                sessions_data = json.load(f)
            
            with self._lock:
                for data in sessions_data:
                    if len(self._sessions) < self.max_sessions:
                        session = Session.from_dict(data)
                        self._sessions[session.session_id] = session
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            logger.warning(f"Could not load sessions from {self._save_path}: {e}")
            with self._lock:
                self._sessions = OrderedDict()

    def save_sessions(self):
        if not self._save_path.parent.exists():
            self._save_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a copy under lock to minimize lock duration and avoid concurrent modification errors during I/O
        with self._lock:
            serializable_sessions = [session.to_dict() for session in self._sessions.values()]
        
        try:
            with open(self._save_path, 'w') as f:
                json.dump(serializable_sessions, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving sessions to disk: {e}")

    def get_session(self, session_id: str) -> Optional[Session]:
        with self._lock:
            if session_id in self._sessions:
                session = self._sessions[session_id]
                self._sessions.move_to_end(session_id)
                session.touch()
                return session
        return None

    def create_session(self, ip_address: str, user_agent: str) -> Session:
        self.cleanup_expired_sessions()
        
        with self._lock:
            if len(self._sessions) >= self.max_sessions:
                self._sessions.popitem(last=False)
            
            session = Session(ip_address, user_agent)
            self._sessions[session.session_id] = session
        
        self.save_sessions()
        return session

    def cleanup_expired_sessions(self):
        now = time.time()
        expired_ids = []
        
        with self._lock:
            for sid, session in self._sessions.items(): 
                if now - session.last_seen > self.timeout_seconds:
                    expired_ids.append(sid)
            
            for sid in expired_ids:
                del self._sessions[sid]
        
        if expired_ids:
            self.save_sessions()

# Initialize global instance
# Using settings.BASE_DIR to locate the data directory
SAVE_PATH = settings.BASE_DIR / "storage" / "db" / "sessions.json"
session_manager = SessionManager(save_path=SAVE_PATH)
