#!/usr/bin/env python3
"""
🚀 PredictPesa Server Starter
============================

Simple script to start the PredictPesa server with minimal setup.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_minimal_env():
    """Set up minimal environment variables for development."""
    env_vars = {
        "APP_NAME": "PredictPesa",
        "DEBUG": "true",
        "ENVIRONMENT": "development",
        "SECRET_KEY": "dev-secret-key-change-in-production",
        "GROQ_API_KEY": "gsk-dev-key-placeholder",
        "DATABASE_URL": "sqlite:///./predictpesa.db",
        "REDIS_URL": "redis://localhost:6379/0",
        "LOG_LEVEL": "INFO"
    }
    
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
    
    print("✅ Environment variables set")


def check_dependencies():
    """Check if required packages are available."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "groq"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("💡 Install with: pip install fastapi uvicorn pydantic sqlalchemy groq")
        return False
    
    print("✅ All required packages available")
    return True


def start_server():
    """Start the FastAPI server."""
    print("🚀 Starting PredictPesa server...")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Import and run
        import uvicorn
        uvicorn.run(
            "predictpesa.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        print("💡 Try running: pip install -r requirements.txt")


def main():
    """Main function."""
    print("🚀 PredictPesa Server Starter")
    print("=" * 40)
    
    # Setup environment
    setup_minimal_env()
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Start server
    start_server()
    return 0


if __name__ == "__main__":
    sys.exit(main())
