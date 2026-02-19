def weighted_score(skill_match: float, experience: float, tools: float, impact: float) -> float:
    return (
        skill_match * 0.35 +
        experience * 0.20 +
        tools * 0.15 +
        impact * 0.30
    )
