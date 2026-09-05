import re

class AuthSchema:
    @staticmethod
    def validate_registration(data):
        errors = {}
        name = data.get("name", "").strip() if isinstance(data.get("name"), str) else ""
        email = data.get("email", "").strip().lower() if isinstance(data.get("email"), str) else ""
        password = data.get("password", "") if isinstance(data.get("password"), str) else ""

        if not name or len(name) < 2:
            errors["name"] = "Name must be at least 2 characters long."
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors["email"] = "A valid email address is required."
        if not password or len(password) < 6:
            errors["password"] = "Password must be at least 6 characters long."

        return errors

    @staticmethod
    def validate_login(data):
        errors = {}
        email = data.get("email", "").strip().lower() if isinstance(data.get("email"), str) else ""
        password = data.get("password", "") if isinstance(data.get("password"), str) else ""

        if not email:
            errors["email"] = "Email is required."
        if not password:
            errors["password"] = "Password is required."

        return errors
