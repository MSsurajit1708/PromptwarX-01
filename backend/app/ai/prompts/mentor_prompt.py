def build_mentor_prompt(project_title, user_message, context, history):
    return (
        f"You are the dedicated AI Project Mentor for '{project_title}'.\n"
        f"Project Context: {context}\n"
        f"Recent History: {history}\n"
        f"Student Question: {user_message}\n"
        "Provide direct, actionable, step-by-step guidance tailored to the student's level."
    )
