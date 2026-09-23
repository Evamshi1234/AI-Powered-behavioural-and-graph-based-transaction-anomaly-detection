"""Seed a demo patient profile. Run from backend/: python seed_demo.py"""

from app.database import Base, SessionLocal, engine
from app.models import PatientProfile

Base.metadata.create_all(bind=engine)

demo = PatientProfile(
    name="Alex Rivera",
    age=52,
    gender="female",
    conditions="Type 2 diabetes, hypertension",
    medications="Metformin 500mg twice daily, Lisinopril 10mg daily",
    allergies="Penicillin",
    health_goals="Lower A1C, walk 30 minutes daily, reduce sodium intake",
)

with SessionLocal() as db:
    existing = db.query(PatientProfile).filter(PatientProfile.name == demo.name).first()
    if existing:
        print(f"Demo profile already exists (id={existing.id})")
    else:
        db.add(demo)
        db.commit()
        db.refresh(demo)
        print(f"Created demo profile id={demo.id}")
