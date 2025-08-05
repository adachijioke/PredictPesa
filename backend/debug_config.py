#!/usr/bin/env python3
"""
Debug configuration loading.
"""

import traceback
from rich.console import Console

console = Console()

def debug_config():
    """Debug configuration loading."""
    
    console.print("🔍 Debugging configuration...")
    
    try:
        console.print("1. Importing config module...")
        from predictpesa.core.config import settings
        
        console.print("2. Checking CORS settings...")
        console.print(f"CORS Origins: {settings.cors_origins} (type: {type(settings.cors_origins)})")
        console.print(f"CORS Methods: {settings.cors_methods} (type: {type(settings.cors_methods)})")
        console.print(f"CORS Headers: {settings.cors_headers} (type: {type(settings.cors_headers)})")
        
        console.print("3. Checking other settings...")
        console.print(f"Database URL: {settings.database_url}")
        console.print(f"Debug: {settings.debug}")
        console.print(f"Environment: {settings.environment}")
        
        console.print("✅ Configuration loaded successfully!")
        
    except Exception as e:
        console.print(f"❌ Configuration error: {e}")
        console.print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_config()
