#!/usr/bin/env python3
"""
Startup script for the IEEE Paper Generator backend.
This script will check the setup and start the server.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load backend/.env for local startup; Docker injects the same values via env_file.
load_dotenv()

def check_requirements():
    """Check if all required packages are installed"""
    print("Checking requirements...")
    
    try:
        import fastapi
        import uvicorn
        import supabase
        import google.genai
        import PyPDF2
        import docx
        import langchain
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    required = ("SUPABASE_URL", "SUPABASE_KEY", "GEMINI_API_KEY")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        print("✗ Missing required environment variables: " + ", ".join(missing))
        print("Set them in backend/.env or in your deployment environment.")
        return False

    print("✓ Required environment variables found")
    return True

def create_upload_dir():
    """Create upload directory if it doesn't exist"""
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    print("✓ Upload directory ready")

def main():
    """Main startup function"""
    print("IEEE Paper Generator Backend Startup")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Check environment
    if not check_env_file():
        return 1
    
    # Create necessary directories
    create_upload_dir()
    
    print("\n🚀 Starting server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"✗ Server failed to start: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())