from datetime import datetime
from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

T = TypeVar('T')
D = TypeVar('D', bound=BaseModel)


class PaginationMeta(BaseModel):
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    page_size: Optional[int] = None
    current_page: Optional[int] = None
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None


class Meta(BaseModel):
    status: int
    message: Optional[str] = None
    request_time: float = 0.0


class PaginatedResponse(BaseModel, Generic[T]):
    pagination: Optional[PaginationMeta] = None
    items: Optional[List[T]] = None


class SingleResponse(BaseModel, Generic[T]):
    item: Optional[T] = None


class ApiResponse(BaseModel, Generic[T]):
    meta: Meta
    data: Optional[T] = None
