from openai import OpenAI

from app.config import settings
from app.services.safety import DISCLAIMER

SYSTEM_PROMPT = f"""You are a compassionate Personalized Healthcare Assistant.

Rules:
1. {DISCLAIMER}
2. Personalize guidance using the patient's profile (age, conditions, medications, allergies, goals).
3. Use retrieved knowledge snippets when relevant; cite concepts plainly without fabricating studies.
4. Never provide definitive diagnoses or prescribe drugs/doses.
5. Encourage clinician follow-up for concerning or persistent symptoms.
6. If emergency language appears, urge immediate emergency services.
7. Keep answers structured, concise, and actionable (bullets when helpful).
"""


def build_profile_context(profile) -> str:
    return (
        f"Name: {profile.name}\n"
        f"Age: {profile.age}\n"
        f"Gender: {profile.gender}\n"
        f"Conditions: {profile.conditions or 'none listed'}\n"
        f"Medications: {profile.medications or 'none listed'}\n"
        f"Allergies: {profile.allergies or 'none listed'}\n"
        f"Health goals: {profile.health_goals or 'none listed'}"
    )


def _demo_reply(user_message: str, profile_context: str, rag_context: str) -> str:
    msg = user_message.lower()
    lines = [
        "Based on your health profile and trusted wellness knowledge:",
        "",
    ]

    if any(k in msg for k in ["medication", "pill", "dose", "drug"]):
        lines.append("- Review your current medications with your clinician before any changes.")
        lines.append("- Use reminders to improve adherence and log side effects.")
    elif any(k in msg for k in ["diet", "food", "eat", "nutrition"]):
        lines.append("- Emphasize whole foods, fiber, lean protein, and hydration aligned with your conditions.")
        lines.append("- Limit ultra-processed foods and monitor portions if blood sugar or BP is a concern.")
    elif any(k in msg for k in ["exercise", "walk", "workout", "fitness"]):
        lines.append("- Start with low-impact activity (e.g., brisk walking) if cleared by your doctor.")
        lines.append("- Target gradual progression toward 150 minutes/week of moderate activity.")
    elif any(k in msg for k in ["sleep", "stress", "anxiety", "mood"]):
        lines.append("- Prioritize consistent sleep schedule, daylight exposure, and stress-reduction habits.")
        lines.append("- Seek professional support if symptoms persist beyond two weeks.")
    else:
        lines.append("- I can help with lifestyle guidance, medication adherence tips, and preventive care planning.")
        lines.append("- Share specific symptoms or goals for more tailored suggestions.")

    if rag_context:
        lines.extend(["", "Relevant knowledge:", rag_context.split("\n\n")[0][:280] + "..."])

    lines.extend([
        "",
        "Personalization context applied from your profile.",
        f"\n{DISCLAIMER}",
    ])
    return "\n".join(lines)


async def generate_reply(
    user_message: str,
    profile,
    history: list[dict],
    rag_context: str,
) -> tuple[str, str]:
    profile_context = build_profile_context(profile)
    provider = settings.llm_provider

    if provider == "openai" and settings.openai_api_key:
        client = OpenAI(api_key=settings.openai_api_key)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.append({
            "role": "system",
            "content": f"Patient profile:\n{profile_context}\n\nRetrieved knowledge:\n{rag_context}",
        })
        for item in history[-8:]:
            messages.append({"role": item["role"], "content": item["content"]})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.4,
            max_tokens=700,
        )
        text = response.choices[0].message.content or ""
        return text.strip(), "openai"

    return _demo_reply(user_message, profile_context, rag_context), "demo"
