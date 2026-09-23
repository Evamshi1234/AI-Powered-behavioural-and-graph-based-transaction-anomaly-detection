from sqlalchemy.orm import Session

from app.models import PatientProfile


DEMO_PROFILES = [
    {
        "name": "Jordan Lee",
        "age": 52,
        "gender": "non_binary",
        "conditions": "Type 2 diabetes, hypertension",
        "medications": "Metformin, Lisinopril",
        "allergies": "Penicillin",
        "health_goals": "Improve A1C and daily walking habit",
    },
    {
        "name": "Maria Santos",
        "age": 34,
        "gender": "female",
        "conditions": "Asthma",
        "medications": "Albuterol inhaler",
        "allergies": "Pollen, dust mites",
        "health_goals": "Reduce trigger exposure and sleep better",
    },
]


def seed_if_empty(db: Session) -> None:
    if db.query(PatientProfile).count() > 0:
        return
    for data in DEMO_PROFILES:
        db.add(PatientProfile(**data))
    db.commit()
