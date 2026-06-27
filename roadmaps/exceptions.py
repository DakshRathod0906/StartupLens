class CircularDependencyError(Exception):
    """Raised when a dependency graph contains a cycle."""
    pass
