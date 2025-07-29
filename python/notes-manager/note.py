from datetime import datetime
from typing import List, Optional
import yaml

class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None, created: Optional[datetime] = None,
                 author: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []
        self.created = created if created is not None else datetime.now()
        self.author = author
        self.status = status
        self.priority = priority
        





        return None