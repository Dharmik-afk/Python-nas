import pytest
from pathlib import Path
from unittest.mock import MagicMock
from app.core.templates import templates

def test_file_card_component_rendering():
    # Mock item (mimicking a Path object with is_dir, is_file, name, suffix)
    mock_item = MagicMock()
    mock_item.is_dir.return_value = False
    mock_item.is_file.return_value = True
    mock_item.name = "test_file.txt"
    mock_item.suffix = ".txt"
    
    # Mock loop object for Jinja2
    mock_loop = MagicMock()
    mock_loop.index0 = 0
    
    context = {
        "item": mock_item,
        "path": "test_folder",
        "pmask": "r",
        "loop": mock_loop
    }
    
    rendered = templates.get_template("partials/components/file_card.html").render(context)
    
    assert "test_file.txt" in rendered
    assert "bi-download" in rendered # Action button
    assert "txt.svg" in rendered # Icon
    assert "TXT" in rendered # Badge
    assert "rename-btn" not in rendered # Should be hidden with pmask 'r'

def test_folder_card_component_rendering():
    # Mock item
    mock_item = MagicMock()
    mock_item.is_dir.return_value = True
    mock_item.is_file.return_value = False
    mock_item.name = "my_folder"
    
    mock_loop = MagicMock()
    mock_loop.index0 = 1
    
    context = {
        "item": mock_item,
        "path": "",
        "pmask": "rwmda",
        "loop": mock_loop
    }
    
    rendered = templates.get_template("partials/components/file_card.html").render(context)
    
    assert "my_folder" in rendered
    assert "folder.svg" in rendered
    assert "rename-btn" in rendered # Should be visible with pmask 'm'
    assert "delete-btn" in rendered # Should be visible with pmask 'd'

def test_action_bar_rendering():
    context = {
        "pmask": "rw",
        "path": "test"
    }
    rendered = templates.get_template("partials/components/action_bar.html").render(context)
    assert "CREATE FOLDER" in rendered
    assert "UPLOAD FILES" in rendered

def test_action_bar_read_only():
    context = {
        "pmask": "r",
        "path": "test"
    }
    rendered = templates.get_template("partials/components/action_bar.html").render(context)
    assert "CREATE FOLDER" not in rendered
    assert "UPLOAD FILES" not in rendered

def test_action_overlay_rendering():
    context = {
        "item": MagicMock(is_dir=lambda: False),
        "rel_path": "file.txt",
        "pmask": "rwdm"
    }
    rendered = templates.get_template("partials/components/action_overlay.html").render(context)
    assert "bi-download" in rendered
    assert "rename-btn" in rendered
    assert "delete-btn" in rendered

