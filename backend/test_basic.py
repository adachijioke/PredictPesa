#!/usr/bin/env python3
"""
🧪 Basic PredictPesa Tests
=========================

Simple tests to verify the core functionality without external dependencies.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that core modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from predictpesa.core.config import Settings
        print("✅ Config module imported successfully")
        
        from predictpesa.models.base import Base
        print("✅ Base model imported successfully")
        
        from predictpesa.schemas.market import MarketCreate
        print("✅ Market schemas imported successfully")
        
        from predictpesa.services.ai import AIService
        print("✅ AI service imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config():
    """Test configuration loading."""
    print("\n⚙️ Testing configuration...")
    
    try:
        # Set minimal required env vars
        os.environ.setdefault("GROQ_API_KEY", "test-key")
        os.environ.setdefault("SECRET_KEY", "test-secret")
        os.environ.setdefault("DATABASE_URL", "postgresql://test")
        
        from predictpesa.core.config import Settings
        settings = Settings()
        
        print(f"✅ App name: {settings.app_name}")
        print(f"✅ Environment: {settings.environment}")
        print(f"✅ Debug mode: {settings.debug}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n📋 Testing schemas...")
    
    try:
        from predictpesa.schemas.market import MarketCreate
        from datetime import datetime, timedelta
        
        # Test market creation schema
        market_data = MarketCreate(
            title="Test Market",
            description="A test prediction market",
            question="Will this test pass?",
            category="technology",
            end_date=datetime.utcnow() + timedelta(days=30)
        )
        
        print(f"✅ Market schema: {market_data.title}")
        
        from predictpesa.schemas.auth import LoginRequest
        
        login_data = LoginRequest(
            email="test@example.com",
            password="testpassword"
        )
        
        print(f"✅ Auth schema: {login_data.email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False


def test_services():
    """Test service classes."""
    print("\n🔧 Testing services...")
    
    try:
        # Test AI service initialization (without API calls)
        os.environ.setdefault("GROQ_API_KEY", "test-key")
        
        from predictpesa.services.ai import AIService
        ai_service = AIService()
        
        print("✅ AI service initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Service test failed: {e}")
        return False


def main():
    """Run all basic tests."""
    print("🚀 PredictPesa Basic Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Schemas", test_schemas),
        ("Services", test_services)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} tests...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} tests passed")
        else:
            print(f"❌ {test_name} tests failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All basic tests passed! The core system is working.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
