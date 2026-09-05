def build_feature_generation_prompt(title, description):
    return (
        f"For the project '{title}' ({description}), generate a prioritized feature backlog categorized into:\n"
        "1. MVP Features\n2. Intermediate Features\n3. Advanced Features\n4. Future Scope\n"
        "Return a strictly valid JSON object with keys: mvp, intermediate, advanced, future."
    )
