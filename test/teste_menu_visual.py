#!/usr/bin/env python3
"""
Script de teste do novo menu visual
"""

import os
from pathlib import Path

# Carregar variáveis de ambiente do .env
env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

import sys
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

console = Console()

def exibir_menu():
    """Exibe o novo menu visual centralizado."""
    console.clear()
    
    # Cabeçalho estilizado
    header = Panel(
        "[bold cyan]╔════════════════════════════════════╗\n"
        "║     PEBBL_ - Gerenciador de         ║\n"
        "║        Contatos v1.0                ║\n"
        "╚════════════════════════════════════╝[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )
    
    # Menu como tabela
    menu_table = Table(show_header=False, show_footer=False, padding=(0, 2), border_style="dim cyan")
    menu_table.add_column(style="cyan", no_wrap=True, width=8)
    menu_table.add_column(style="white")
    
    menu_items = [
        ("[ 1 ]", "[bold green]➕ Adicionar[/bold green] novo contato"),
        ("[ 2 ]", "[bold blue]📋 Listar[/bold blue] todos os contatos"),
        ("[ 3 ]", "[bold yellow]🔍 Buscar[/bold yellow] contato"),
        ("[ 4 ]", "[bold magenta]✏️  Modificar[/bold magenta] contato"),
        ("[ 5 ]", "[bold red]❌ Remover[/bold red] contato"),
        ("[ 6 ]", "[bold cyan]💾 Exportar[/bold cyan] dados"),
        ("[ 0 ]", "[bold red]🚪 Sair[/bold red]"),
    ]
    
    for num, desc in menu_items:
        menu_table.add_row(num, desc)
    
    # Centralizar conteúdo
    console.print(Align.center(header))
    console.print()
    console.print(Align.center(menu_table))
    console.print()

if __name__ == "__main__":
    exibir_menu()
    console.print("\n[bold cyan]✅ Menu visual funcionando![/bold cyan]")
