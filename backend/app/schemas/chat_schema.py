class ChatSchema:
    @staticmethod
    def validate_message(data):
        errors = {}
        msg = data.get("message", "").strip() if isinstance(data.get("message"), str) else ""
        if not msg:
            errors["message"] = "Message text cannot be empty."
        if len(msg) > 2000:
            errors["message"] = "Message cannot exceed 2000 characters."
        return errors
