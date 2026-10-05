"""CLI entry point for the SK hynix DART pipeline.

The script lives under scripts/, so make the repository root importable
before importing the agent package. This works both locally and in GitHub
Actions when invoked as: python scripts/run_pipeline.py.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.pipeline import main


if __name__ == "__main__":
    main()
