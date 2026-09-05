class TaskSchema:
    VALID_STATUSES = {"NOT_STARTED", "IN_PROGRESS", "COMPLETED", "BLOCKED"}
    VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    @classmethod
    def validate_task(cls, data):
        errors = {}
        if not data.get("title") or len(data["title"].strip()) < 2:
            errors["title"] = "Task title is required."
        if "status" in data and data["status"] not in cls.VALID_STATUSES:
            errors["status"] = f"Status must be one of {cls.VALID_STATUSES}"
        if "priority" in data and data["priority"] not in cls.VALID_PRIORITIES:
            errors["priority"] = f"Priority must be one of {cls.VALID_PRIORITIES}"

        return errors
