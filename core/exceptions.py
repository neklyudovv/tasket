class TasketError(Exception):
    message = "error occurred"

    def __str__(self):
        return self.message


class UserAlreadyExistsError(TasketError):
    message = "user already exists"


class InvalidCredentialsError(TasketError):
    message = "invalid credentials"


class TaskNotFoundError(TasketError):
    message = "task not found"


class PermissionDeniedError(TasketError):
    message = "permission denied"
