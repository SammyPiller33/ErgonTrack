from abc import ABC, abstractmethod
from typing import List, Optional
from tasktracker.task import Task


class TaskRepository(ABC):
    """Interface for task data access operations"""

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Retrieve all tasks"""
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID"""
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        """Save or update a task"""
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """Delete a task by its ID"""
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """Get the next available task ID"""
        pass