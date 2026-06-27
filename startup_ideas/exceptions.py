class StartupIdeaError(Exception):
    """Base exception for startup ideas"""
    pass

class VersionConflictError(StartupIdeaError):
    """Raised when an optimistic lock check fails during update"""
    pass

class DuplicateIdeaError(StartupIdeaError):
    """Raised when a duplicate idea is detected and strictly rejected"""
    pass
