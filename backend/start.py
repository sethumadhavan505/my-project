#!/usr/bin/env python3
"""Startup script for the IEEE Paper Generator backend."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Always run relative paths (uploads, model cache, etc.) from backend/.
BACKEND_DIR = Path(__file__).resolve().parent
os.chdir(BACKEND_DIR)
load_dotenv(BACKEND_DIR / ".env")

def check_requirements():
    """Check that the core backend packages are installed."""
    print("Checking requirements...")
    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
        import supabase  # noqa: F401
        import google.genai  # noqa: F401
        import PyPDF2  # noqa: F401
        import docx  # noqa: F401
        import langchain  # noqa: F401
        print("✓ Core backend packages are installed")
        return True
    except ImportError as exc:
        print(f"✗ Missing package: {exc}")
        print("Run: python -m pip install -r requirements.txt")
        return False

def check_env_file():
    """Validate the environment variables needed by the API."""
    required = ("SUPABASE_URL", "SUPABASE_KEY", "GEMINI_API_KEY")
    missing = [key for key in required if not os.getenv(key, "").strip()]
    if missing:
        print("✗ Missing required environment variables: " + ", ".join(missing))
        print(f"Add them to {BACKEND_DIR / '.env'}")
        return False
    print("✓ Required environment variables found")
    return True

def main():
    print("IEEE Research Paper Generator - Backend")
    print("=" * 44)

    if not check_requirements() or not check_env_file():
        return 1

    (BACKEND_DIR / "uploads").mkdir(exist_ok=True)
    print("✓ Upload directory ready")
    print("\nStarting FastAPI server...")
    print("API:  http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop")
    print("=" * 44)

    try:
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    except Exception as exc:
        print(f"✗ Backend failed to start: {exc}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
