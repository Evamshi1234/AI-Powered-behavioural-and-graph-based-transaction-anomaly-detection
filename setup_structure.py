"""
UPI-Shield — One-time setup script
Run this ONCE from your upi-shield folder to create the correct structure.
Usage: python setup_structure.py
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

DIRS = [
    "phase1/feature_engineering", "phase1/feature_store", "phase1/security", "phase1/tests",
    "phase2/transformer", "phase2/gnn", "phase2/mlops",
    "phase3/microservices", "phase3/kafka",
    "phase4/rl_engine", "phase4/autoscaling",
]

FILE_MAP = {
    "pipeline.py": "phase1/feature_engineering/pipeline.py",
    "store.py": "phase1/feature_store/store.py",
    "hardening.py": "phase1/security/hardening.py",
    "test_phase1.py": "phase1/tests/test_phase1.py",
    "tracker.py": "phase2/mlops/tracker.py",
    "services.py": "phase3/microservices/services.py",
    "streaming.py": "phase3/kafka/streaming.py",
    "ppo_agent.py": "phase4/rl_engine/ppo_agent.py",
    "k8s_and_chaos.py": "phase4/autoscaling/k8s_and_chaos.py",
}
MODEL_PY_DEST = "phase2/transformer/model.py"


def main():
    print("=== UPI-Shield Structure Setup ===\n")
    for directory in DIRS:
        full = os.path.join(HERE, directory)
        os.makedirs(full, exist_ok=True)
        init = os.path.join(full, "__init__.py")
        if not os.path.exists(init):
            open(init, "w").close()

    for phase in ["phase1", "phase2", "phase3", "phase4"]:
        init = os.path.join(HERE, phase, "__init__.py")
        if not os.path.exists(init):
            open(init, "w").close()

    root_init = os.path.join(HERE, "__init__.py")
    if not os.path.exists(root_init):
        open(root_init, "w").close()

    moved = skipped = 0
    for src_name, dest_rel in FILE_MAP.items():
        src, dest = os.path.join(HERE, src_name), os.path.join(HERE, dest_rel)
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"  ✓ {src_name} → {dest_rel}")
            moved += 1
        elif os.path.exists(dest):
            print(f"  ✓ {dest_rel} already in place")
        else:
            print(f"  ⚠ NOT FOUND: {src_name}")
            skipped += 1

    src, dest = os.path.join(HERE, "model.py"), os.path.join(HERE, MODEL_PY_DEST)
    if os.path.exists(src) and not os.path.exists(dest):
        shutil.copy2(src, dest)
        print(f"  ✓ model.py → {MODEL_PY_DEST}")

    print(f"\n✓ Moved {moved} files, skipped {skipped}")
    print("\n=== Testing imports ===")
    sys.path.insert(0, HERE)
    tests = [
        ("phase1.feature_engineering.pipeline", ["FeaturePipeline", "Transaction"]),
        ("phase1.feature_store.store", ["FeatureStore"]),
        ("phase1.security.hardening", ["SecurityLayer"]),
        ("phase2.mlops.tracker", ["ExperimentTracker", "DriftDetector"]),
        ("phase3.kafka.streaming", ["create_producer", "TOPICS"]),
        ("phase4.rl_engine.ppo_agent", ["FraudEnvironment", "PPOTrainer"]),
        ("phase4.autoscaling.k8s_and_chaos", ["CircuitBreaker", "ChaosMonkey"]),
    ]
    errors = []
    for module, names in tests:
        try:
            __import__(module, fromlist=names)
            print(f"  ✓ {module}")
        except Exception as exc:
            print(f"  ✗ {module}: {exc}")
            errors.append(module)
    if errors:
        print(f"\n⚠ {len(errors)} import(s) failed. Check the files above.")
    else:
        print("\n✅ All imports OK! Run: python main.py")


if __name__ == "__main__":
    main()
