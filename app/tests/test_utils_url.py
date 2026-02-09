import os
import pytest
from unittest.mock import patch, mock_open
import stat
from app.core.utils import get_public_url, generate_opener_script

def test_get_public_url_env_var():
    """Test that PUBLIC_URL environment variable takes precedence."""
    with patch.dict(os.environ, {"PUBLIC_URL": "https://cool-tunnel.com"}):
        url = get_public_url(8000, "0.0.0.0")
        assert url == "https://cool-tunnel.com"

def test_get_public_url_lan_ip():
    """Test that it resolves to LAN IP when host is 0.0.0.0 and no env var."""
    with patch("app.core.utils.get_lan_ip", return_value="192.168.1.50"):
        # Ensure PUBLIC_URL is not set
        with patch.dict(os.environ, {}, clear=True):
            url = get_public_url(8000, "0.0.0.0")
            assert url == "http://192.168.1.50:8000"

def test_get_public_url_localhost():
    """Test that it returns localhost/127.0.0.1 if explicitly set."""
    with patch.dict(os.environ, {}, clear=True):
        url = get_public_url(8000, "127.0.0.1")
        assert url == "http://127.0.0.1:8000"

def test_get_public_url_custom_host():
    """Test that it respects a custom host."""
    with patch.dict(os.environ, {}, clear=True):
        url = get_public_url(9090, "my-server.local")
        assert url == "http://my-server.local:9090"

def test_generate_opener_script():
    """Test that the script is generated with the correct content and permissions."""
    mock_file = mock_open()
    
    with patch("builtins.open", mock_file), \
         patch("os.chmod") as mock_chmod, \
         patch("app.core.utils.get_public_url", return_value="http://192.168.1.100:8000"):
        
        generate_opener_script(8000, "0.0.0.0")
        
        # Verify file write
        mock_file.assert_called_with("open_server.sh", "w")
        handle = mock_file()
        
        expected_content = (
            "#!/bin/bash\n"
            "am start -a android.intent.action.VIEW -d \"http://192.168.1.100:8000\" > /dev/null 2>&1 &\n"
        )
        handle.write.assert_called_once_with(expected_content)
        
        # Verify chmod
        mock_chmod.assert_called_once_with("open_server.sh", 0o755)
        
        