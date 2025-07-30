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
        self.modified = self.created  # Assuming modified is set to created initially
        self.author = author
        self.status = status
        self.priority = priority
    
    def to_yaml(self) -> str:
        """Convert the note to a YAML string."""
        # Filter out None values for YAML header
        head = {k: v for k, v in {
            'title': self.title,
            'content': self.content,
            'created': self.created,
            'modified': self.modified,
            'tags': self.tags,
            'author': self.author,
            'status': self.status,
            'priority': self.priority
        }.items() if v is not None}
        return f"---\n{yaml.dump(head)}---\n{self.content}"

        
