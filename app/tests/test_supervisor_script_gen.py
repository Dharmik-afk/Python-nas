import sys
from unittest.mock import patch, MagicMock
import pytest

# Add project root to sys.path so we can import supervisor
sys.path.append(".")
from supervisor.supervisor import main

def test_supervisor_generates_script():
    """Test that supervisor main function calls generate_opener_script."""
    
    with (
        patch("supervisor.supervisor.start_copyparty") as mock_cp,
        patch("supervisor.supervisor.start_uvicorn") as mock_uvi,
        patch("supervisor.supervisor.check_health", return_value=True),
        patch("supervisor.supervisor.generate_opener_script") as mock_gen,
        patch("supervisor.supervisor.time.sleep", side_effect=[None, None, None, InterruptedError("Break Loop")]),
        patch("supervisor.supervisor.signal") as mock_signal,
        patch("supervisor.supervisor.settings") as mock_settings
    ):
        
        mock_settings.FRONTEND_PORT = 8000
        mock_settings.FRONTEND_HOST = "0.0.0.0"

        try:
            main()
        except (InterruptedError, AttributeError):
            pass
        
        # Verify it was called
        mock_gen.assert_called_once_with(8000, "0.0.0.0")
        
        