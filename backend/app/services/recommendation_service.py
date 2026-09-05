from app.models.project import Project

class RecommendationService:
    @staticmethod
    def filter_projects(filters, page=1, limit=20):
        query = Project.query.filter_by(status='ACTIVE')
        if filters.get("domain"):
            query = query.filter(Project.domain.ilike(f"%{filters['domain']}%"))
        if filters.get("difficulty"):
            query = query.filter(Project.difficulty.ilike(f"%{filters['difficulty']}%"))
        if filters.get("duration"):
            query = query.filter(Project.duration.ilike(f"%{filters['duration']}%"))

        total = query.count()
        items = query.order_by(Project.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
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
