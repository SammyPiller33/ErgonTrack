from typing import List, Optional
from tasktracker.task import Task, TaskStatus
from tasktracker.task_repository import TaskRepository


class TaskService:
    """Service for task business logic"""

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def add_task(self, description: str) -> Task:
        """Add a new task"""
        task_id = self.repository.get_next_id()
        new_task = Task(id=task_id, description=description)
        self.repository.save(new_task)
        return new_task

    def update_task(self, task_id: int, description: Optional[str] = None,
                    status: Optional[str] = None) -> Task:
        """Update an existing task"""
        task = self.repository.get_by_id(task_id)

        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        if description:
            task.update_description(description)

        if status:
            status_code = TaskStatus.from_string(status)
            task.update_status(status_code)

        self.repository.save(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task"""
        task = self.repository.get_by_id(task_id)

        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        self.repository.delete(task_id)

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """List all tasks, optionally filtered by status"""
        tasks = self.repository.get_all()

        if status:
            status_code = TaskStatus.from_string(status)
            return [task for task in tasks if task.status == status_code]

        return tasks

    def mark_in_progress(self, task_id: int) -> Task:
        """Mark a task as in progress"""
        return self.update_task(task_id, status="in-progress")

    def mark_done(self, task_id: int) -> Task:
        """Mark a task as done"""
        return self.update_task(task_id, status="done")