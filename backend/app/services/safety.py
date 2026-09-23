import re

EMERGENCY_PATTERNS = [
    r"\bchest pain\b",
    r"\bcan(?:'|no)t breathe\b",
    r"\bstroke\b",
    r"\bheart attack\b",
    r"\bunconscious\b",
    r"\bsevere bleeding\b",
    r"\bsuicid",
    r"\boverdose\b",
]

DISCLAIMER = (
    "This assistant provides general health information only and is not a substitute "
    "for professional medical advice, diagnosis, or treatment."
)


def detect_emergency(text: str) -> list[str]:
    lowered = text.lower()
    flags: list[str] = []
    for pattern in EMERGENCY_PATTERNS:
        if re.search(pattern, lowered):
            flags.append("possible_emergency")
            break
    return flags


def emergency_response() -> str:
    return (
        "Your message may indicate a medical emergency. "
        "Call your local emergency number immediately (e.g., 911 in the US) "
        "or go to the nearest emergency department. "
        "Do not rely on this chat for urgent care."
    )
