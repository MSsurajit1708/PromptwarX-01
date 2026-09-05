class RoadmapSchema:
    @staticmethod
    def validate_roadmap(data):
        errors = {}
        if not data.get("phase_name"):
            errors["phase_name"] = "Phase name is required."
        if "phase_order" not in data or not isinstance(data.get("phase_order"), int):
            errors["phase_order"] = "Phase order must be an integer."
        return errors
