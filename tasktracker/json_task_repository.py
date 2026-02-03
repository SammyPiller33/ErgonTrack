import json
import os
from typing import List, Optional
from tasktracker.task import Task
from tasktracker.task_repository import TaskRepository


class JsonTaskRepository(TaskRepository):
    """JSON file implementation of TaskRepository"""

    def __init__(self, file_path: str = "./tasks.json"):
        self.file_path = file_path

    def get_all(self) -> List[Task]:
        """Retrieve all tasks from JSON file"""
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stored_tasks = data.get('tasks', [])
                return [Task(**task_dict) for task_dict in stored_tasks]
        except (json.JSONDecodeError, IOError) as e:
            raise Exception(f"Error reading tasks file: {e}")

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID"""
        tasks = self.get_all()
        return next((task for task in tasks if task.id == task_id), None)

    def save(self, task: Task) -> None:
        """Save or update a task to JSON file"""
        tasks = self.get_all()

        # Remove existing task with same ID if it exists
        tasks = [t for t in tasks if t.id != task.id]
        tasks.append(task)

        self._write_all(tasks)

    def delete(self, task_id: int) -> None:
        """Delete a task by its ID"""
        self._write_all([t for t in self.get_all() if t.id != task_id])

    def get_next_id(self) -> int:
        """Get the next available task ID"""
        tasks = self.get_all()
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

    def _write_all(self, tasks: List[Task]) -> None:
        """Internal method to write all tasks to file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                tasks_dict = {
                    'tasks': [task.to_dict() for task in tasks]
                }
                json.dump(tasks_dict, f, indent=4, ensure_ascii=False)
        except IOError as e:
            raise Exception(f"Error writing tasks file: {e}")