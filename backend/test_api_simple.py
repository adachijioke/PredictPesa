#!/usr/bin/env python3
"""
Simple API test to debug the issue.
"""

import asyncio
import httpx
from rich.console import Console

console = Console()

async def test_api():
    """Test API endpoints directly."""
    
    console.print("🔍 Testing API endpoints...")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        # Test health endpoint
        try:
            console.print("Testing /health...")
            response = await client.get("http://localhost:8001/health")
            console.print(f"Health status: {response.status_code}")
            console.print(f"Health response: {response.json()}")
        except Exception as e:
            console.print(f"Health error: {e}")
        
        # Test markets endpoint
        try:
            console.print("Testing /markets...")
            response = await client.get("http://localhost:8001/markets")
            console.print(f"Markets status: {response.status_code}")
            console.print(f"Markets response: {response.json()}")
        except Exception as e:
            console.print(f"Markets error: {e}")
        
        # Test AI endpoint
        try:
            console.print("Testing /ai/analyze...")
            response = await client.post(
                "http://localhost:8001/ai/analyze",
                json={"query": "test query"}
            )
            console.print(f"AI status: {response.status_code}")
            console.print(f"AI response: {response.json()}")
        except Exception as e:
            console.print(f"AI error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
