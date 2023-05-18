# @classmethod
# def paginate(cls: Type[P], base: URL, offset: int, limit: int, count: int) -> P:
#     after = offset + limit

#     if after > count:
#         next = None

#     else:
#         next = base.with_query(offset=after, limit=limit)

#     before = offset - limit

#     if before < 0:
#         before = 0

#     if offset:
#         previous = base.with_query(offset=before, limit=limit)

#     else:
#         previous = None

#     return cls(previous=previous, next=next, count=count)
