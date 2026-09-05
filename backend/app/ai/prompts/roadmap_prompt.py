def build_roadmap_prompt(title, description):
    return (
        f"Create a step-by-step engineering roadmap for building '{title}' ({description}).\n"
        "Divide into phases: Research, Architecture/Planning, Backend API, Frontend UI, AI/Integration, Testing & Deployment.\n"
        "Return a JSON array of objects with keys: phase_name, phase_order, description."
    )
