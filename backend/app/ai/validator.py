class AIValidator:
    @staticmethod
    def validate_project_list(projects):
        if not isinstance(projects, list):
            return False
        for p in projects:
            if not isinstance(p, dict) or "title" not in p or "description" not in p:
                return False
        return True
