import pytest
from unittest.mock import MagicMock
from fastapi import Request
from app.core.templates import auth_context

def test_auth_context_processor():
    # Mock Request
    request = MagicMock(spec=Request)
    
    # Mock Session with data
    session = MagicMock()
    session.username = "testuser"
    session.permissions = "rw"
    request.state.session = session
    
    context = auth_context(request)
    assert context["user_permissions"] == "rw"
    assert context["username"] == "testuser"

def test_auth_context_processor_no_session():
    # Mock Request
    request = MagicMock(spec=Request)
    request.state.session = None
    
    context = auth_context(request)
    assert context["user_permissions"] == ""
    assert context["username"] == ""
