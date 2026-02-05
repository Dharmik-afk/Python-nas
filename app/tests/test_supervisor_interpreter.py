import sys
import os
from unittest.mock import patch

from supervisor.supervisor import start_copyparty, start_uvicorn

def test_supervisor_uses_current_interpreter():
    """
    Test that supervisor functions use sys.executable instead of hardcoded 'python3'.
    This ensures that if we run with PyPy, the children also use PyPy.
    """
    with patch("subprocess.Popen") as mock_popen:
        # We need to mock settings because start_copyparty uses them
        with patch("supervisor.supervisor.settings") as mock_settings:
            mock_settings.COPYPARTY_HOST = "127.0.0.1"
            mock_settings.COPYPARTY_PORT = 8090
            mock_settings.FRONTEND_HOST = "0.0.0.0"
            mock_settings.FRONTEND_PORT = 8000
            
            # Test start_copyparty
            start_copyparty()
            args, _ = mock_popen.call_args
            cmd = args[0]
            assert cmd[0] == sys.executable, f"Expected {sys.executable}, got {cmd[0]}"
            
            # Reset mock
            mock_popen.reset_mock()
            
            # Test start_uvicorn
            start_uvicorn()
            args, _ = mock_popen.call_args
            cmd = args[0]
            assert cmd[0] == sys.executable, f"Expected {sys.executable}, got {cmd[0]}"

def test_supervisor_propagates_env():
    """
    Test that supervisor propagates the environment (including VIRTUAL_ENV) to children.
    """
    with patch("subprocess.Popen") as mock_popen:
        with patch("supervisor.supervisor.settings") as mock_settings:
            mock_settings.FRONTEND_HOST = "0.0.0.0"
            mock_settings.FRONTEND_PORT = 8000
            
            # Setup a fake VIRTUAL_ENV
            with patch.dict(os.environ, {"VIRTUAL_ENV": "/fake/venv"}):
                start_uvicorn()
                _, kwargs = mock_popen.call_args
                # By default Popen inherits env if env=None is passed or if env is not passed.
                # In current implementation, it's not passed, so it's None.
                assert kwargs.get("env") is None