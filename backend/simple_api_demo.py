#!/usr/bin/env python3
"""
Simple API Demo for PredictPesa Backend
Tests the basic API endpoints without database dependencies.
"""

import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

BASE_URL = "http://localhost:8001"

def test_endpoint(endpoint, description):
    """Test an API endpoint and display results."""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            console.print(f"✅ {description}")
            console.print(Panel(json.dumps(data, indent=2), title=f"Response from {endpoint}"))
            return True
        else:
            console.print(f"❌ {description} - Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        console.print(f"❌ {description} - Error: {e}")
        return False

def main():
    """Run the API demo."""
    console.print(Panel.fit("🚀 PredictPesa API Demo", style="bold blue"))
    
    # Check if server is running
    console.print("\n🔍 Checking server status...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            console.print("❌ Server not responding correctly")
            return False
    except requests.exceptions.RequestException:
        console.print("❌ Server not running. Start with: python simple_server.py")
        return False
    
    console.print("✅ Server is running!")
    
    # Test endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/v1/markets", "Markets endpoint"),
        ("/api/v1/ai/analyze", "AI analysis endpoint"),
    ]
    
    results = []
    for endpoint, description in endpoints:
        console.print(f"\n🧪 Testing {description}...")
        success = test_endpoint(endpoint, description)
        results.append((endpoint, description, success))
    
    # Summary
    console.print("\n" + "="*60)
    console.print("📊 Test Results Summary")
    console.print("="*60)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Endpoint", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Status", style="green")
    
    passed = 0
    for endpoint, description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        if success:
            passed += 1
        table.add_row(endpoint, description, status)
    
    console.print(table)
    
    # Final summary
    total = len(results)
    if passed == total:
        console.print(Panel.fit(f"🎉 All {total} tests passed! API is working correctly.", style="bold green"))
    else:
        console.print(Panel.fit(f"⚠️  {passed}/{total} tests passed. Some endpoints need attention.", style="bold yellow"))
    
    console.print(f"\n📖 API Documentation: {BASE_URL}/docs")
    console.print(f"🔍 Health Check: {BASE_URL}/health")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n👋 Demo interrupted by user")
        exit(1)
    except Exception as e:
        console.print(f"\n❌ Demo failed with error: {e}")
        exit(1)
