def build_architecture_prompt(title, technologies):
    return (
        f"Design the end-to-end system architecture for '{title}' using technologies {technologies}.\n"
        "Return a JSON object with keys: architecture_type, components, data_flow, communication_flow, explanation, scalability_considerations."
    )
