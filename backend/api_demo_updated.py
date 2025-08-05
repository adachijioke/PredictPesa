#!/usr/bin/env python3
"""
PredictPesa API Demo - Updated Version
Demonstrates the core functionality of the PredictPesa prediction market platform.

This script tests:
- Basic API endpoints
- Health checks and monitoring  
- Market data retrieval
- AI analysis features
- Performance testing

Usage:
    python api_demo_updated.py

Requirements:
    - PredictPesa backend server running on port 8001
    - Network connectivity
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import httpx
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api/v1"

# Initialize Rich console
console = Console()

class PredictPesaDemo:
    """PredictPesa API demonstration client."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def print_header(self, title: str, emoji: str = "🚀"):
        """Print a beautiful header."""
        console.print()
        console.print(Panel(
            f"[bold cyan]{emoji} {title}[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))
    
    async def test_endpoint(self, name: str, url: str, expected_keys: list = None):
        """Test an API endpoint and record results."""
        try:
            start_time = time.time()
            response = await self.client.get(url)
            end_time = time.time()
            
            response_time = round((end_time - start_time) * 1000, 2)  # ms
            
            if response.status_code == 200:
                data = response.json()
                
                # Check expected keys if provided
                missing_keys = []
                if expected_keys:
                    missing_keys = [key for key in expected_keys if key not in data]
                
                self.test_results.append({
                    "name": name,
                    "status": "✅ PASS",
                    "response_time": f"{response_time}ms",
                    "status_code": response.status_code,
                    "data": data,
                    "missing_keys": missing_keys
                })
                
                console.print(f"[green]✅ {name}[/green] - {response_time}ms")
                return data
            else:
                self.test_results.append({
                    "name": name,
                    "status": "❌ FAIL",
                    "response_time": f"{response_time}ms",
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}"
                })
                console.print(f"[red]❌ {name}[/red] - HTTP {response.status_code}")
                return None
                
        except Exception as e:
            self.test_results.append({
                "name": name,
                "status": "❌ ERROR",
                "error": str(e)
            })
            console.print(f"[red]❌ {name}[/red] - Error: {e}")
            return None
    
    async def demo_health_check(self):
        """Demonstrate health check functionality."""
        self.print_header("Health Check & Status", "🏥")
        
        # Test health endpoint
        health_data = await self.test_endpoint(
            "Health Check", 
            f"{BASE_URL}/health",
            ["status", "service", "version", "environment"]
        )
        
        if health_data:
            # Display health information
            health_table = Table(title="System Health")
            health_table.add_column("Metric", style="cyan")
            health_table.add_column("Value", style="green")
            
            for key, value in health_data.items():
                health_table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(health_table)
    
    async def demo_markets(self):
        """Demonstrate market functionality."""
        self.print_header("Prediction Markets", "📈")
        
        # Test markets endpoint
        markets_data = await self.test_endpoint(
            "Markets List",
            f"{API_BASE}/markets",
            ["markets", "total"]
        )
        
        if markets_data and "markets" in markets_data:
            # Display markets
            markets_table = Table(title="Available Markets")
            markets_table.add_column("ID", style="cyan")
            markets_table.add_column("Title", style="white", width=30)
            markets_table.add_column("Category", style="green")
            markets_table.add_column("Status", style="blue")
            markets_table.add_column("Yes Prob", style="green")
            markets_table.add_column("No Prob", style="red")
            
            for market in markets_data["markets"]:
                markets_table.add_row(
                    market.get("id", "N/A"),
                    market.get("title", "N/A")[:27] + "..." if len(market.get("title", "")) > 30 else market.get("title", "N/A"),
                    market.get("category", "N/A").title(),
                    market.get("status", "N/A").title(),
                    f"{market.get('yes_probability', 0):.2%}",
                    f"{market.get('no_probability', 0):.2%}"
                )
            
            console.print(markets_table)
            
            # Display market statistics
            total_markets = markets_data.get("total", 0)
            console.print(f"\n[cyan]📊 Total Markets: {total_markets}[/cyan]")
    
    async def demo_ai_analysis(self):
        """Demonstrate AI analysis functionality."""
        self.print_header("AI Market Analysis", "🤖")
        
        # Test AI analysis endpoint
        ai_data = await self.test_endpoint(
            "AI Analysis",
            f"{API_BASE}/ai/analyze",
            ["analysis", "confidence", "recommendation"]
        )
        
        if ai_data:
            # Display AI analysis
            console.print(Panel(
                f"""
[bold cyan]🧠 AI Market Analysis[/bold cyan]

[white]Analysis:[/white] {ai_data.get('analysis', 'N/A')}

[white]Confidence:[/white] [green]{ai_data.get('confidence', 0):.1%}[/green]

[white]Recommendation:[/white] [yellow]{ai_data.get('recommendation', 'N/A')}[/yellow]
                """,
                border_style="blue",
                title="AI Insights"
            ))
    
    async def demo_performance_test(self):
        """Demonstrate performance testing."""
        self.print_header("Performance Testing", "⚡")
        
        console.print("Running performance tests...")
        
        # Test multiple requests
        endpoints = [
            ("Root", f"{BASE_URL}/"),
            ("Health", f"{BASE_URL}/health"),
            ("Markets", f"{API_BASE}/markets"),
            ("AI Analysis", f"{API_BASE}/ai/analyze")
        ]
        
        performance_results = []
        
        for name, url in endpoints:
            times = []
            for i in range(5):  # 5 requests per endpoint
                start_time = time.time()
                try:
                    response = await self.client.get(url)
                    end_time = time.time()
                    if response.status_code == 200:
                        times.append((end_time - start_time) * 1000)
                except:
                    pass
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                performance_results.append({
                    "endpoint": name,
                    "avg_time": avg_time,
                    "min_time": min_time,
                    "max_time": max_time,
                    "requests": len(times)
                })
        
        # Display performance results
        if performance_results:
            perf_table = Table(title="Performance Results (5 requests each)")
            perf_table.add_column("Endpoint", style="cyan")
            perf_table.add_column("Avg Time", style="green")
            perf_table.add_column("Min Time", style="blue")
            perf_table.add_column("Max Time", style="red")
            perf_table.add_column("Requests", style="white")
            
            for result in performance_results:
                perf_table.add_row(
                    result["endpoint"],
                    f"{result['avg_time']:.1f}ms",
                    f"{result['min_time']:.1f}ms",
                    f"{result['max_time']:.1f}ms",
                    str(result["requests"])
                )
            
            console.print(perf_table)
    
    async def demo_summary(self):
        """Display demo summary."""
        self.print_header("Demo Summary", "📋")
        
        # Test results summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if "PASS" in r["status"]])
        failed_tests = total_tests - passed_tests
        
        # Summary table
        summary_table = Table(title="Test Results Summary")
        summary_table.add_column("Test", style="cyan", width=25)
        summary_table.add_column("Status", style="white")
        summary_table.add_column("Response Time", style="green")
        summary_table.add_column("Details", style="yellow")
        
        for result in self.test_results:
            details = ""
            if result.get("missing_keys"):
                details = f"Missing: {', '.join(result['missing_keys'])}"
            elif result.get("error"):
                details = result["error"]
            
            summary_table.add_row(
                result["name"],
                result["status"],
                result.get("response_time", "N/A"),
                details
            )
        
        console.print(summary_table)
        
        # Overall summary
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        if success_rate == 100:
            status_color = "green"
            status_emoji = "🎉"
            status_text = "All tests passed!"
        elif success_rate >= 75:
            status_color = "yellow"
            status_emoji = "⚠️"
            status_text = "Most tests passed"
        else:
            status_color = "red"
            status_emoji = "❌"
            status_text = "Several tests failed"
        
        console.print(Panel(
            f"""
{status_emoji} [bold {status_color}]{status_text}[/bold {status_color}]

[cyan]Test Results:[/cyan]
✅ Passed: {passed_tests}
❌ Failed: {failed_tests}
📊 Success Rate: {success_rate:.1f}%

[cyan]Features Tested:[/cyan]
✅ Health monitoring
✅ Market data retrieval
✅ AI analysis integration
✅ Performance metrics
✅ API response validation

[yellow]🌍 PredictPesa API Demo Complete![/yellow]
            """,
            border_style=status_color,
            title="Final Summary"
        ))
    
    async def run_demo(self):
        """Run the complete demo."""
        console.print(Panel(
            """
🚀 [bold cyan]PredictPesa API Demo[/bold cyan]

Africa's first DeFi-native prediction market platform
built on Hedera blockchain.

[green]Testing core API functionality...[/green]
            """,
            border_style="cyan"
        ))
        
        try:
            await self.demo_health_check()
            await self.demo_markets()
            await self.demo_ai_analysis()
            await self.demo_performance_test()
            await self.demo_summary()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Demo failed: {e}[/red]")
            import traceback
            console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")

async def main():
    """Main demo function."""
    async with PredictPesaDemo() as demo:
        await demo.run_demo()

def check_server():
    """Check if server is running."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5.0)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Check server status
    console.print("[blue]🔍 Checking server status...[/blue]")
    
    is_running, result = check_server()
    
    if is_running:
        console.print("[green]✅ Server is running![/green]")
        console.print(f"[cyan]Server Info: {result.get('service', 'Unknown')} v{result.get('version', 'Unknown')}[/cyan]")
        asyncio.run(main())
    else:
        console.print(f"[red]❌ Server not running: {result}[/red]")
        console.print("[yellow]💡 Start server with: python simple_server.py[/yellow]")
