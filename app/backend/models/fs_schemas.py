from pydantic import BaseModel
from typing import List, Optional

class FSItem(BaseModel):
    name: str
    path: str
    is_dir: bool
    size: int
    mtime: float
    permissions: str

class DirectoryListing(BaseModel):
    path: str
    items: List[FSItem]
    permissions: str # Permissions for the directory itself
