def build_project_generation_prompt(profile_data):
    return (
        "You are ProjectMentor AI, an expert academic and industry advisor for final-year engineering/CS students.\n"
        f"Generate 6-8 tailored, realistic, non-trivial, portfolio-worthy project ideas for the following profile:\n"
        f"- Skills: {', '.join(profile_data.get('skills', []))}\n"
        f"- Interests: {', '.join(profile_data.get('interests', []))}\n"
        f"- Academic Branch: {profile_data.get('branch', 'Computer Science')}\n"
        f"- Career Goal: {profile_data.get('careerGoal', 'Software Engineer')}\n"
        f"- Experience Level: {profile_data.get('experience', 'Intermediate')}\n"
        f"- Duration: {profile_data.get('duration', '8 weeks')}\n\n"
        "Return a strictly valid JSON array of objects with keys: title, description, problem_statement, solution, domain, difficulty, duration, target_users, technologies, core_features, advanced_features, innovation_score, feasibility_score, career_relevance_score, reason_for_recommendation."
    )
