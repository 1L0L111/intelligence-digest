from app.models import UserProfile

def apply_feedback(profile: UserProfile, terms: list[str], positive: bool=True) -> UserProfile:
    data=profile.model_dump(); interests=list(data['interests']); priorities=dict(data['priorities'])
    for term in terms:
        if positive and term not in interests: interests.append(term)
        priorities[term]=max(0.1,min(2.0,priorities.get(term,1.0)+(0.15 if positive else -0.25)))
    data['interests']=interests; data['priorities']=priorities
    return UserProfile(**data)
