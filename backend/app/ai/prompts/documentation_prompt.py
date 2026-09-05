def build_documentation_prompt(title):
    return (
        f"Generate a structured university project report outline for '{title}'.\n"
        "Include sections: Abstract, Introduction, Problem Statement, System Architecture, Database Design, Implementation, Testing Results, and Future Scope."
    )
