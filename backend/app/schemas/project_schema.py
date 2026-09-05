class ProjectSchema:
    VALID_DIFFICULTIES = {"Easy", "Beginner", "Medium", "Intermediate", "Hard", "Advanced"}
    VALID_STATUSES = {"ACTIVE", "IN_PROGRESS", "COMPLETED", "ARCHIVED"}

    @classmethod
    def validate_project(cls, data):
        errors = {}
        if not data.get("title") or len(data["title"].strip()) < 3:
            errors["title"] = "Project title is required and must be at least 3 characters."
        if not data.get("description") or len(data["description"].strip()) < 10:
            errors["description"] = "Description is required and must be at least 10 characters."

        return errors
