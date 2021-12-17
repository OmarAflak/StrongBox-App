from typing import Generic, Optional, TypeVar
from dataclasses import dataclass
from strongbox.locker.io import IO

T = TypeVar("T", bound=IO)


@dataclass
class APIError:
    code: int
    message: Optional[str] = None


@dataclass
class APIResponse(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[APIError] = None

    @classmethod
    def on_success(cls, data: T) -> 'APIResponse[T]':
        return cls(success=True, data=data, error=None)

    @classmethod
    def on_fail(cls, error: Optional[APIError] = None) -> 'APIResponse[T]':
        return cls(success=False, data=None, error=error)
