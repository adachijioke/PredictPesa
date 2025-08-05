#!/usr/bin/env python3
"""
🔧 PredictPesa Environment Setup
===============================

Sets up a clean development environment for PredictPesa.
"""

import subprocess
import sys
import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


def create_virtual_environment():
    """Create a virtual environment."""
    console.print("[blue]🐍 Creating virtual environment...[/blue]")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        console.print("[green]✅ Virtual environment created![/green]")
        
        # Determine activation script path
        if os.name == 'nt':  # Windows
            activate_script = "venv\\Scripts\\activate"
        else:  # Unix/Linux/macOS
            activate_script = "source venv/bin/activate"
        
        console.print(f"[yellow]💡 Activate with: {activate_script}[/yellow]")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to create virtual environment: {e}[/red]")
        return False


def install_dependencies():
    """Install dependencies using requirements.txt."""
    console.print("[blue]📦 Installing dependencies...[/blue]")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_path = "venv/bin/pip"
    
    try:
        # Upgrade pip first
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # Install from requirements.txt
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        
        console.print("[green]✅ Dependencies installed successfully![/green]")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to install dependencies: {e}[/red]")
        return False


def setup_environment_file():
    """Set up the .env file."""
    console.print("[blue]⚙️ Setting up environment configuration...[/blue]")
    
    if Path(".env").exists():
        overwrite = Confirm.ask("⚠️ .env file already exists. Overwrite?", default=False)
        if not overwrite:
            console.print("[yellow]Keeping existing .env file[/yellow]")
            return True
    
    # Copy from example
    try:
        import shutil
        shutil.copy(".env.example", ".env")
        console.print("[green]✅ .env file created from template[/green]")
        
        console.print()
        console.print("[yellow]🔑 Please update the following in .env:[/yellow]")
        console.print("• GROQ_API_KEY=gsk-your-groq-api-key")
        console.print("• HEDERA_ACCOUNT_ID=your-hedera-account")
        console.print("• HEDERA_PRIVATE_KEY=your-hedera-private-key")
        console.print("• SECRET_KEY=your-secure-secret-key")
        
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Failed to create .env file: {e}[/red]")
        return False


def check_system_requirements():
    """Check system requirements."""
    console.print("[blue]🔍 Checking system requirements...[/blue]")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 11):
        console.print(f"[red]❌ Python 3.11+ required, found {python_version.major}.{python_version.minor}[/red]")
        return False
    
    console.print(f"[green]✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}[/green]")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        console.print("[red]❌ Please run this script from the project root directory[/red]")
        return False
    
    console.print("[green]✅ Project structure looks good[/green]")
    return True


def main():
    """Main setup function."""
    console.print(Panel(
        """
🔧 [bold cyan]PredictPesa Environment Setup[/bold cyan]

This script will:
1. Check system requirements
2. Create a virtual environment
3. Install all dependencies
4. Set up configuration files

[green]Let's get your development environment ready![/green]
        """,
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Check system requirements
    if not check_system_requirements():
        return
    
    # Ask if user wants to proceed
    if not Confirm.ask("🚀 Ready to set up the environment?", default=True):
        console.print("[yellow]Setup cancelled by user[/yellow]")
        return
    
    # Create virtual environment
    if not create_virtual_environment():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Setup environment file
    if not setup_environment_file():
        return
    
    # Success message
    console.print()
    console.print(Panel(
        """
🎉 [bold green]Environment Setup Complete![/bold green]

[cyan]Next Steps:[/cyan]
1. Activate the virtual environment:
   • Linux/macOS: source venv/bin/activate
   • Windows: venv\\Scripts\\activate

2. Update your .env file with real credentials

3. Start the server:
   python -m uvicorn predictpesa.main:app --reload

4. Visit: http://localhost:8000/docs

[yellow]Happy coding! 🚀[/yellow]
        """,
        border_style="green",
        padding=(1, 2)
    ))


if __name__ == "__main__":
    main()
