def build_viva_prompt(title):
    return (
        f"Generate 8-10 likely Viva Voce / defense examination questions with model answers for '{title}'.\n"
        "Categorize into: Basic, Technical, Architecture, Database, AI/ML, Security, Testing, Future Scope."
    )
