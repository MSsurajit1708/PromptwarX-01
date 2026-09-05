def build_career_prompt(title, technologies):
    return (
        f"Analyze the career and placement value for a student project titled '{title}' using {technologies}.\n"
        "Return JSON with: skills_demonstrated, technologies_learned, resume_bullets, github_readme_pitch, interview_talking_points."
    )
