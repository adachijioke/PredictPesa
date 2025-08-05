#!/usr/bin/env python3
"""
🚀 PredictPesa Setup and Demo Runner
===================================

Quick setup script to install dependencies and run the demo.
"""

import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def install_dependencies():
    """Install project dependencies."""
    console.print("[blue]📦 Installing dependencies...[/blue]")
    
    try:
        # Install in editable mode
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True, capture_output=True, text=True)
        
        console.print("[green]✅ Dependencies installed successfully![/green]")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to install dependencies: {e}[/red]")
        console.print(f"[red]Error output: {e.stderr}[/red]")
        return False


def run_server():
    """Run the FastAPI server."""
    console.print("[blue]🚀 Starting PredictPesa server...[/blue]")
    console.print("[yellow]Press Ctrl+C to stop the server[/yellow]")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "predictpesa.main:app", 
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], check=True)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped by user[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Server failed: {e}[/red]")


def main():
    """Main setup and run function."""
    console.print(Panel(
        """
🚀 [bold cyan]PredictPesa Backend Setup[/bold cyan]

This will:
1. Install all dependencies
2. Start the FastAPI server
3. Launch the API documentation

[green]Ready to build the future of prediction markets![/green]
        """,
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        console.print("[red]❌ Please run this script from the project root directory[/red]")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Show next steps
    console.print()
    console.print(Panel(
        """
🎉 [bold green]Setup Complete![/bold green]

[cyan]Next Steps:[/cyan]
1. Set your Groq API key in .env: GROQ_API_KEY=gsk-your-key
2. Run the server: python -m uvicorn predictpesa.main:app --reload
3. Visit API docs: http://localhost:8000/docs
4. Run the demo: python api_demo.py

[yellow]The server will start automatically now...[/yellow]
        """,
        border_style="green",
        padding=(1, 2)
    ))
    
    # Start server
    run_server()


if __name__ == "__main__":
    main()
