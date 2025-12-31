import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from fastapi import Request
from app.backend.services.copyparty_service import proxy_stream_request
from starlette.responses import StreamingResponse

@pytest.mark.anyio
async def test_proxy_stream_request_unicode_filename_crash():
    # Setup mock request
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}
    
    # Non-ASCII filename that caused the crash
    unicode_filename = "Boys பொളിയா.mp4"
    relative_path = Path(unicode_filename)
    
    # Mock requests.get response
    mock_response = MagicMock()
    mock_response.status_code = 206
    mock_response.headers = {
        'Content-Type': 'video/mp4',
        'Content-Length': '100',
        'Accept-Ranges': 'bytes'
    }
    mock_response.iter_content.return_value = [b"data"]
    
    with patch("app.backend.services.copyparty_service.requests.get", return_value=mock_response), \
         patch("app.backend.services.copyparty_service.get_proxy_headers", return_value={}), \
         patch("app.backend.services.copyparty_service._get_proxy_url", return_value="http://127.0.0.1:8090/file"):
        
        # This call will fail with UnicodeEncodeError
        response = await proxy_stream_request(
            request=mock_request,
            relative_path=relative_path,
            params={"media": ""}
        )

