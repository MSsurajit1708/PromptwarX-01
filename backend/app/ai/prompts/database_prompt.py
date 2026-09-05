def build_database_prompt(title, description):
    return (
        f"Design the database schema for '{title}' ({description}).\n"
        "Return a JSON object with keys: database_type, tables (with fields, data types, primary_key, foreign_keys), relationships, index_recommendations."
    )
