def build_analysis_prompt(project_data):
    return (
        f"Perform a comprehensive code and architectural analysis for the project: {project_data.get('title')}.\n"
        "Evaluate strengths, weaknesses, missing features, technical improvements, security improvements, scalability improvements, UI/UX improvements, and overall quality score."
    )
