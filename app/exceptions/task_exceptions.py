class TaskNotFound(Exception):
    status_code = 404
    detail = "Task not found"