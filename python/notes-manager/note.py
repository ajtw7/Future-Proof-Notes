from datetime import datetime
from typing import List, Optional
import yaml
import uuid

class Note:
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None, created: Optional[datetime] = None,
                 author: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, note_id: Optional[str] = None):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []
        self.created = created if created is not None else datetime.now()
        self.modified = self.created  # Assuming modified is set to created initially
        self.author = author
        self.status = status
        self.priority = priority
        self.note_id = note_id if note_id is not None else str(uuid.uuid4()) # Generate a unique ID if not provided

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
            'priority': self.priority,
            'note_id': self.note_id
        }.items() if v is not None}
        return f"---\n{yaml.dump(head)}---\n{self.content}"

        
