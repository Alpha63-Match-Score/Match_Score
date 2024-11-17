from fastapi import Query

class PaginationParams:
    def __init__(self, offset: int, limit: int):
        self.offset = offset
        self.limit = limit

def get_pagination(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> PaginationParams:

    return PaginationParams(offset=offset, limit=limit)
