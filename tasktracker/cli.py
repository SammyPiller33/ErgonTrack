import argparse
from tasktracker.task import TaskStatus
from tasktracker.json_task_repository import JsonTaskRepository
from tasktracker.task_service import TaskService
from tasktracker.logger import get_logger
from tasktracker.ascii_art import LOGO

"""
Task Tracker CLI - Command line interface for managing tasks.

This module provides the main CLI interface for the task tracker application,
including command parsing and execution of task operations.
"""

def init_logger():
    """Get logger"""

    print(LOGO)
    logger = get_logger(__name__)

    return logger

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Task Tracker CLI")

    subparsers = parser.add_subparsers(dest="action", required=True, help="Action to perform")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("description", help="Description of the task to be added")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", help="Description to update")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Mark-in-progress command
    mark_in_progress_parser = subparsers.add_parser("mark-in-progress", help="Mark a task as in progress")
    mark_in_progress_parser.add_argument("id", type=int, help="Task ID")

    # Mark-done command
    mark_done_parser = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_done_parser.add_argument("id", type=int, help="Task ID")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "status",
        nargs='?',
        choices=list(TaskStatus.get_all_statuses().keys()),
        default=None,
        help="Filter by status (optional)"
    )

    return parser.parse_args()


def run():
    """Main entry point for the CLI"""
    
    logger = init_logger()
    
    args = parse_args()
    logger.info(f"Running action '{args.action}'")
    
    # Initialize repository and service (Dependency Injection)
    repository = JsonTaskRepository("./tasks.json")
    service = TaskService(repository)

    try:
        if args.action == "add":
            task = service.add_task(args.description)
            logger.info(f"Task added successfully (ID: {task.id})")

        elif args.action == "update":
            task = service.update_task(args.id, description=args.description)
            logger.info(f"Task {task.id} updated successfully")

        elif args.action == "delete":
            service.delete_task(args.id)
            logger.info(f"Task {args.id} deleted successfully")

        elif args.action == "mark-in-progress":
            task = service.mark_in_progress(args.id)
            logger.info(f"Task {task.id} marked as in progress")

        elif args.action == "mark-done":
            task = service.mark_done(args.id)
            logger.info(f"Task {task.id} marked as done")

        elif args.action == "list":
            tasks = service.list_tasks(args.status)
            if tasks:
                logger.info(f"Tasks ({len(tasks)}):")
                for task in tasks:
                    logger.info(f"  - [ID: {task.id}] {task.description} (Status: {task.status})")
            else:
                logger.info("No tasks found")

    except ValueError as e:
        logger.info(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.info(f"Unexpected error: {e}")
        exit(1)
