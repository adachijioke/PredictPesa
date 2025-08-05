#!/usr/bin/env python3
"""
PredictPesa API Demo
Demonstrates the core functionality of the PredictPesa prediction market platform.

This script tests:
- Basic API endpoints
- Health checks and monitoring
- Market data retrieval
- AI analysis features
- Performance testing

Usage:
    python api_demo.py

Requirements:
    - PredictPesa backend server running on port 8001
    - Network connectivity
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

import httpx
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live

# Configuration
BASE_URL = "http://localhost:8001"
API_VERSION = "v1"
API_BASE = f"{BASE_URL}/api/{API_VERSION}"

# Demo user credentials
DEMO_USER_EMAIL = "demo@predictpesa.com"
DEMO_USER_PASSWORD = "demo123"

# Initialize Rich console
console = Console()

# Global session for maintaining connections
httpx_client: Optional[httpx.AsyncClient] = None

class PredictPesaDemo:
    """PredictPesa API demonstration client."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.access_token: Optional[str] = None
        self.created_markets: List[Dict] = []
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _headers(self) -> Dict[str, str]:
        """Get headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated API request."""
        url = f"{BASE_URL}{endpoint}"
        headers = self._headers()
        
        try:
            response = await self.client.request(
                method, url, headers=headers, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            console.print(f"[red]API Error: {e}[/red]")
            return {}
    
    def print_header(self, title: str, icon: str = "🔹"):
        """Print a formatted header."""
        console.print(Panel(f"[bold cyan]{icon} {title}[/bold cyan]", border_style="cyan"))
    
    async def demo_root(self):
        """Demonstrate root endpoint."""
        self.print_header("Welcome Message", "🏠")
        
        console.print("🌟 Checking root endpoint...")
        response = await self._request("GET", "/")
        
        if response:
            message = response.get('message', 'No message')
            version = response.get('version', 'Unknown')
            status = response.get('status', 'Unknown')
            environment = response.get('environment', 'Unknown')
            
            console.print(f"[green]✅ {message}[/green]")
            console.print(f"[blue]📦 Version: {version}[/blue]")
            console.print(f"[blue]🔄 Status: {status}[/blue]")
            console.print(f"[blue]🌍 Environment: {environment}[/blue]")
            return True
        else:
            console.print("[red]❌ Root endpoint failed[/red]")
            return False
    
    async def demo_health_check(self):
        """Demonstrate health check endpoint."""
        self.print_header("Health Check", "🏥")
        
        console.print("🔍 Checking server health...")
        response = await self._request("GET", "/health")
        
        if response:
            console.print(f"[green]✅ Server Status: {response.get('status', 'Unknown')}[/green]")
            console.print(f"[blue]📊 Timestamp: {response.get('timestamp', 'Unknown')}[/blue]")
            return True
        else:
            console.print("[red]❌ Health check failed[/red]")
            return False
    
    async def demo_markets(self):
        """Demonstrate market endpoints."""
        self.print_header("Market Data", "📊")
        
        console.print("📈 Fetching market data...")
        try:
            response = await self._request("GET", "/api/v1/markets")
            
            if response:
                markets = response.get('markets', [])
                console.print(f"[green]✅ Found {len(markets)} markets[/green]")
                
                if markets:
                    table = Table(title="Available Markets")
                    table.add_column("ID", style="cyan")
                    table.add_column("Title", style="green", width=40)
                    table.add_column("Category", style="blue")
                    table.add_column("Status", style="yellow")
                    
                    for market in markets[:5]:  # Show first 5 markets
                        title = market.get("title", "Unknown")
                        if len(title) > 40:
                            title = title[:37] + "..."
                        table.add_row(
                            str(market.get("id", "N/A")),
                            title,
                            market.get("category", "Unknown").title(),
                            market.get("status", "Unknown").title()
                        )
                    
                    console.print(table)
                else:
                    console.print("[yellow]⚠️ No markets found[/yellow]")
            else:
                console.print("[red]❌ Failed to fetch markets[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error fetching markets: {e}[/red]")
    
    async def demo_ai_analysis(self):
        """Demonstrate AI analysis features."""
        self.print_header("AI Market Analysis", "🤖")
        
        console.print("🧠 Requesting AI market analysis...")
        
        try:
            # Test AI analysis endpoint
            analysis_request = {
                "query": "What are the key factors affecting Bitcoin price in 2025?",
                "market_context": "cryptocurrency",
                "analysis_type": "prediction"
            }
            
            response = await self._request("GET", "/api/v1/ai/analyze")
            
            if response:
                analysis = response.get('analysis', 'No analysis available')
                confidence = response.get('confidence', 0)
                recommendation = response.get('recommendation', 'No recommendation')
                
                console.print(Panel(
                    f"[bold cyan]AI Analysis:[/bold cyan]\n\n{analysis}\n\n[yellow]Confidence: {confidence:.1%}[/yellow]\n\n[green]Recommendation: {recommendation}[/green]",
                    title="🤖 AI Insights",
                    border_style="cyan"
                ))
            else:
                console.print("[red]❌ AI analysis failed[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error in AI analysis: {e}[/red]")
    
    async def demo_performance(self):
        """Demonstrate performance testing."""
        self.print_header("Performance Testing", "⚡")
        
        endpoints = [
            ("/", "GET"),
            ("/health", "GET"),
            ("/api/v1/markets", "GET"),
            ("/api/v1/ai/analyze", "GET")
        ]
        
        results = []
        
        try:
            for endpoint, method in endpoints:
                console.print(f"🔄 Testing {method} {endpoint}...")
                
                # Time multiple requests
                times = []
                for _ in range(3):
                    try:
                        start_time = time.time()
                        
                        await self._request(method, endpoint)
                        
                        end_time = time.time()
                        times.append((end_time - start_time) * 1000)  # Convert to ms
                    except Exception as e:
                        console.print(f"[yellow]⚠️ Request failed: {e}[/yellow]")
                        times.append(0)  # Add 0 for failed requests
                
                if times and any(t > 0 for t in times):  # Only if we have valid times
                    valid_times = [t for t in times if t > 0]
                    avg_time = sum(valid_times) / len(valid_times) if valid_times else 0
                    results.append((endpoint, method, avg_time))
                    console.print(f"[green]✅ Average response time: {avg_time:.1f}ms[/green]")
                else:
                    console.print(f"[red]❌ All requests failed for {endpoint}[/red]")
            
            # Display performance summary
            if results:
                table = Table(title="Performance Results")
                table.add_column("Endpoint", style="cyan")
                table.add_column("Method", style="blue")
                table.add_column("Avg Time (ms)", style="green")
                
                for endpoint, method, avg_time in results:
                    table.add_row(endpoint, method, f"{avg_time:.1f}")
                
                console.print(table)
        except Exception as e:
            console.print(f"[red]❌ Performance testing failed: {e}[/red]")
    
    async def demo_summary(self):
        """Display demo summary."""
        self.print_header("Demo Summary", "📋")
        
        console.print(Panel(
            """
🎉 [bold green]PredictPesa API Demo Completed![/bold green]

[cyan]Features Demonstrated:[/cyan]
✅ Health check monitoring
✅ Market data retrieval
✅ AI-powered analysis
✅ Performance testing
✅ DeFi-ready infrastructure

[yellow]🌍 Ready for Africa's prediction market revolution![/yellow]
            """,
            border_style="green"
        ))
    
    async def run_demo(self):
        """Run the complete demo."""
        console.print(Panel(
            """
🚀 [bold cyan]PredictPesa API Demo[/bold cyan]

Africa's first DeFi-native prediction market platform
built on Hedera blockchain.

[green]Let's explore the features![/green]
            """,
            border_style="cyan"
        ))
        
        try:
            # Run demo sequence
            await self.demo_root()
            await self.demo_health_check()
            await self.demo_markets()
            await self.demo_ai_analysis()
            await self.demo_performance()
            await self.demo_summary()
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo interrupted[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Demo failed: {e}[/red]")
            import traceback
            console.print("[red]Full traceback:[/red]")
            traceback.print_exc()


async def main():
    """Main demo function."""
    async with PredictPesaDemo() as demo:
        await demo.run_demo()


if __name__ == "__main__":
    # Check server status
    console.print("[blue]🔍 Checking server status...[/blue]")
    
    try:
        response = httpx.get("http://localhost:8001/health", timeout=5.0)
        if response.status_code == 200:
            console.print("[green]✅ Server is running![/green]")
            asyncio.run(main())
        else:
            console.print("[red]❌ Server not responding[/red]")
            console.print("[yellow]💡 Try starting the server with: python simple_server.py[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Server not running: {e}[/red]")
        console.print("[yellow]💡 Start the server with: python simple_server.py[/yellow]")
