from dataclasses import dataclass, field
from datetime import datetime as dt
from typing import Dict


class TaskStatus:
    """Task status constants"""
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3

    STATUS_MAP = {
        "todo": TODO,
        "in-progress": IN_PROGRESS,
        "done": DONE
    }

    @classmethod
    def from_string(cls, status: str) -> int:
        """Convert status string to status code"""
        return cls.STATUS_MAP.get(status, cls.TODO)

    @classmethod
    def get_all_statuses(cls) -> Dict[str, int]:
        """Get all available statuses"""
        return cls.STATUS_MAP.copy()


@dataclass
class Task:
    """Task entity"""
    id: int
    description: str
    status: int = field(default=TaskStatus.TODO)
    createdAt: str = field(default_factory=lambda: dt.now().isoformat())
    updatedAt: str = field(default_factory=lambda: dt.now().isoformat())

    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    def update_description(self, description: str) -> None:
        """Update task description"""
        self.description = description
        self.updatedAt = dt.now().isoformat()

    def update_status(self, status: int) -> None:
        """Update task status"""
        self.status = status
        self.updatedAt = dt.now().isoformat()
