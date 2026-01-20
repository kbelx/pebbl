def menu_interativo():
    """Exibe o menu principal interativo."""
    while True:
        limpar_tela()
        
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
        
        opcao = Prompt.ask("[bold cyan]➤ Escolha uma opção[/bold cyan]", choices=["1", "2", "3", "4", "5", "6", "0"], default="0")
        
        if opcao == "0":
            limpar_tela()
            console.print(Align.center(Panel.fit(
                "[bold yellow]👋 Saindo... Até logo![/bold yellow]",
                border_style="yellow",
                padding=(1, 3)
            )))
            break
            
        elif opcao == "1":
            adicionar()
            Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")
            
        elif opcao == "2":
            listar()
            Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")
            
        elif opcao == "3":
            termo = Prompt.ask("[bold]Digite o nome para buscar[/bold]")
            buscar(termo)
            Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")
            
        elif opcao == "4":
            id_str = Prompt.ask("[bold]ID do contato a modificar[/bold]")
            if id_str.isdigit():
                modificar(int(id_str))
            else:
                console.print("[red]❌ ID inválido![/red]")
            Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")
            
        elif opcao == "5":
            id_str = Prompt.ask("[bold]ID do contato a remover[/bold]")
            if id_str.isdigit():
                remover(int(id_str))
            else:
                console.print("[red]❌ ID inválido![/red]")
            Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")
            
        elif opcao == "6":
            formato = Prompt.ask("[bold]Formato[/bold]", choices=["csv", "txt"], default="csv")
            exportar(formato)
            Prompt.ask("\n[dim]Pressione Enter para