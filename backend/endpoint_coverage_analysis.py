#!/usr/bin/env python3
"""
Endpoint Coverage Analysis for PredictPesa API Demo
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def analyze_endpoint_coverage():
    """Analyze which endpoints are available vs tested."""
    
    console.print(Panel(
        "[bold cyan]PredictPesa API Endpoint Coverage Analysis[/bold cyan]",
        border_style="cyan"
    ))
    
    # Available endpoints in simple_server.py
    available_endpoints = [
        {
            "path": "/",
            "method": "GET",
            "function": "root",
            "description": "Root endpoint - Welcome message"
        },
        {
            "path": "/health",
            "method": "GET", 
            "function": "health_check",
            "description": "Health check endpoint"
        },
        {
            "path": "/api/v1/markets",
            "method": "GET",
            "function": "get_markets", 
            "description": "Get markets endpoint (mock data)"
        },
        {
            "path": "/api/v1/ai/analyze",
            "method": "GET",
            "function": "ai_analyze",
            "description": "AI analysis endpoint (mock)"
        }
    ]
    
    # Tested endpoints in api_demo.py
    tested_endpoints = [
        {
            "path": "/",
            "method": "GET",
            "demo_function": "demo_root",
            "tested": True
        },
        {
            "path": "/health",
            "method": "GET",
            "demo_function": "demo_health_check",
            "tested": True
        },
        {
            "path": "/api/v1/markets", 
            "method": "GET",
            "demo_function": "demo_markets",
            "tested": True
        },
        {
            "path": "/api/v1/ai/analyze",
            "method": "GET", 
            "demo_function": "demo_ai_analysis",
            "tested": True
        }
    ]
    
    # Create coverage table
    table = Table(title="Endpoint Coverage Analysis")
    table.add_column("Endpoint", style="cyan")
    table.add_column("Method", style="blue")
    table.add_column("Description", style="white")
    table.add_column("Tested", style="green")
    table.add_column("Demo Function", style="yellow")
    
    tested_paths = {ep["path"] for ep in tested_endpoints}
    
    for endpoint in available_endpoints:
        path = endpoint["path"]
        method = endpoint["method"]
        description = endpoint["description"]
        
        if path in tested_paths:
            tested_status = "✅ YES"
            demo_func = next(
                (ep["demo_function"] for ep in tested_endpoints if ep["path"] == path),
                "N/A"
            )
        else:
            tested_status = "❌ NO"
            demo_func = "Missing"
        
        table.add_row(path, method, description, tested_status, demo_func)
    
    console.print(table)
    
    # Summary
    total_endpoints = len(available_endpoints)
    tested_count = len([ep for ep in available_endpoints if ep["path"] in tested_paths])
    untested_count = total_endpoints - tested_count
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"📊 Total Available Endpoints: {total_endpoints}")
    console.print(f"✅ Tested Endpoints: {tested_count}")
    console.print(f"❌ Untested Endpoints: {untested_count}")
    console.print(f"📈 Coverage: {(tested_count/total_endpoints)*100:.1f}%")
    
    if untested_count > 0:
        console.print(f"\n[yellow]⚠️ Missing Tests:[/yellow]")
        for endpoint in available_endpoints:
            if endpoint["path"] not in tested_paths:
                console.print(f"  • {endpoint['method']} {endpoint['path']} - {endpoint['description']}")
    else:
        console.print(f"\n[green]🎉 All endpoints are covered in the demo![/green]")

if __name__ == "__main__":
    analyze_endpoint_coverage()
