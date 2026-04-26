class DomainError(Exception):
    """Base for business rule errors."""
    status_code: int = 500


class NotFoundError(DomainError):
    """Entity not found."""
    status_code = 404


class ValidationError(DomainError):
    """Invalid input or business rule violation."""
    status_code = 400


class ConflictError(DomainError):
    """Resource conflict (e.g. duplicate)."""
    status_code = 409


class PermissionDeniedError(DomainError):
    """Caller is not allowed to perform this action."""
    status_code = 403


class ConversationNotFoundError(NotFoundError):
    pass

