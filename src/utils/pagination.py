from fastapi import Query
from typing import Optional

class PaginationParams:
    def __init__(self,
            skip: int | None = Query(default=0, ge=0),
            limit: int | None = Query(default=10, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

def get_pagination() -> PaginationParams:
    return PaginationParams()