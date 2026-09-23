# UPI-Shield

AI-powered UPI transaction anomaly and fraud detection platform.

The repository contains the orchestration entry point, MLflow experiment logging helper, location utilities, and package setup script supplied for the project. The full runtime imports the phase modules described by `setup_structure.py`.

## Quick start

```bash
python setup_structure.py
pip install -r requirements.txt
python main.py
```

Optional services such as Redis, Kafka, and MLflow can be run separately; the application is designed to provide fallbacks when they are unavailable.

## Important note

`location.py` includes mock/demo location data only. A phone number prefix does not provide a person's real-time location; production use requires lawful, consent-based carrier or device-location integrations.
