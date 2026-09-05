class ProfileSchema:
    VALID_EXPERIENCE_LEVELS = {"Beginner", "Intermediate", "Advanced"}

    @classmethod
    def validate_update(cls, data):
        errors = {}
        if "semester" in data and data["semester"] is not None:
            try:
                sem = int(data["semester"])
                if sem < 1 or sem > 12:
                    errors["semester"] = "Semester must be between 1 and 12."
            except (ValueError, TypeError):
                errors["semester"] = "Semester must be an integer."

        if "experience_level" in data and data["experience_level"]:
            if data["experience_level"] not in cls.VALID_EXPERIENCE_LEVELS:
                errors["experience_level"] = f"Experience level must be one of {cls.VALID_EXPERIENCE_LEVELS}"

        return errors
