from app.models import DigestEvent, UserProfile

def render_markdown(events: list[DigestEvent], profile: UserProfile) -> str:
    lines = [f"# Intelligence Digest — {profile.role}", "", f"Интересы: {', '.join(profile.interests)}", ""]
    for e in sorted(events, key=lambda x: x.score, reverse=True):
        lines += [f"## {e.title}", "", e.summary, "", f"**Почему важно:** {e.why_it_matters}", "", f"**Score:** {e.score:.0%}", f"**Причины отбора:** {', '.join(e.reasons)}", "", "**Источники:**"]
        lines += [f"- {s}" for s in e.sources]
        lines.append("")
    return "\n".join(lines)
