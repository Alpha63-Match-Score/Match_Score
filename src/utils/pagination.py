from fastapi import Query

class PaginationParams:
    def __init__(self, skip: int, limit: int):
        self.skip = skip
        self.limit = limit

def get_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)
