def calculate_project_score(project, profile_data):
    user_skills = set([s.lower() for s in profile_data.get("skills", [])])
    proj_techs = set([t.lower() for t in project.get("technologies", [])])
    
    # Skill Match (25%)
    if proj_techs:
        matched = len(user_skills.intersection(proj_techs))
        skill_match = min(100, int((matched / len(proj_techs)) * 100) + 40)
    else:
        skill_match = 75

    # Interest Match (20%)
    user_interests = set([i.lower() for i in profile_data.get("interests", [])])
    domain = project.get("domain", "").lower()
    interest_match = 90 if any(i in domain for i in user_interests) else 75

    # Career Relevance (20%)
    career_goal = profile_data.get("careerGoal", "").lower()
    career_relevance = 92 if career_goal in domain or "engineer" in career_goal else 82

    # Feasibility (15%)
    feasibility = project.get("feasibility_score", 85)

    # Innovation (10%)
    innovation = project.get("innovation_score", 80)

    # Difficulty Fit (10%)
    exp_level = profile_data.get("experience", "Intermediate").lower()
    diff = project.get("difficulty", "Intermediate").lower()
    difficulty_fit = 95 if exp_level == diff else 80

    overall_score = round(
        (skill_match * 0.25) +
        (interest_match * 0.20) +
        (career_relevance * 0.20) +
        (feasibility * 0.15) +
        (innovation * 0.10) +
        (difficulty_fit * 0.10), 1
    )

    return {
        "skill_match": skill_match,
        "interest_match": interest_match,
        "career_relevance": career_relevance,
        "feasibility": feasibility,
        "innovation": innovation,
        "difficulty_fit": difficulty_fit,
        "overall_score": overall_score
    }
