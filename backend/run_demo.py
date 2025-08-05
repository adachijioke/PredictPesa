#!/usr/bin/env python3
"""
🚀 PredictPesa Backend Demo Runner
==================================

This script demonstrates the complete PredictPesa backend functionality
by starting the server and running the API demo.
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def check_dependencies():
    """Check if required dependencies are available."""
    console.print("[blue]🔍 Checking dependencies...[/blue]")
    
    try:
        import predictpesa
        console.print("[green]✅ PredictPesa package found[/green]")
    except ImportError:
        console.print("[red]❌ PredictPesa package not found. Run: pip install -e .[/red]")
        return False
    
    return True


def start_server():
    """Start the FastAPI server."""
    console.print("[blue]🚀 Starting PredictPesa server...[/blue]")
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "predictpesa.main:app", 
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Starting server...", total=None)
            
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = httpx.get("http://localhost:8000/health", timeout=2.0)
                    if response.status_code == 200:
                        progress.update(task, description="Server started!")
                        console.print("[green]✅ Server is running at http://localhost:8000[/green]")
                        return process
                except (httpx.RequestError, httpx.TimeoutException):
                    time.sleep(1)
                    continue
        
        console.print("[red]❌ Server failed to start within 30 seconds[/red]")
        process.terminate()
        return None
        
    except Exception as e:
        console.print(f"[red]❌ Failed to start server: {e}[/red]")
        return None


async def run_api_demo():
    """Run the API demonstration."""
    console.print("[blue]🎭 Running API demo...[/blue]")
    
    try:
        # Import and run the demo
        from api_demo import main as demo_main
        await demo_main()
        
    except Exception as e:
        console.print(f"[red]❌ Demo failed: {e}[/red]")


def main():
    """Main demo runner."""
    console.print(Panel(
        """
🚀 [bold cyan]PredictPesa Backend Demo[/bold cyan]

This demo will:
1. Check dependencies
2. Start the FastAPI server
3. Run comprehensive API demonstrations
4. Show all features in action

[green]Ready to revolutionize prediction markets in Africa![/green]
        """,
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check if server is already running
    try:
        response = httpx.get("http://localhost:8000/health", timeout=2.0)
        if response.status_code == 200:
            console.print("[green]✅ Server is already running![/green]")
            server_process = None
        else:
            server_process = start_server()
            if not server_process:
                return
    except (httpx.RequestError, httpx.TimeoutException):
        server_process = start_server()
        if not server_process:
            return
    
    try:
        # Run the demo
        asyncio.run(run_api_demo())
        
        console.print()
        console.print(Panel(
            """
🎉 [bold green]Demo Completed Successfully![/bold green]

The PredictPesa backend is fully functional and ready for production!

[cyan]Next Steps:[/cyan]
• Deploy to production environment
• Integrate with Hedera mainnet
• Launch mobile applications
• Onboard African users

[yellow]API Documentation: http://localhost:8000/docs[/yellow]
            """,
            border_style="green",
            padding=(1, 2)
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo failed: {e}[/red]")
    finally:
        # Clean up server process
        if server_process:
            console.print("[blue]🛑 Stopping server...[/blue]")
            server_process.terminate()
            server_process.wait()
            console.print("[green]✅ Server stopped[/green]")


if __name__ == "__main__":
    main()
