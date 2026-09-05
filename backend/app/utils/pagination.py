def paginate_query(query, page=1, limit=20):
    page = max(1, page)
    limit = min(max(1, limit), 100)
    
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()
    pages = (total + limit - 1) // limit if limit > 0 else 1

    return {
        "items": [item.to_dict() for item in items],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages
        }
    }
