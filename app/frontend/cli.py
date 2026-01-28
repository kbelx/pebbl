import os
import platform
import typer
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align

from app.frontend.menu import menu_interativo


def build_app(controller, console):
    app = typer.Typer(
        help="Pebbl_ - Sistema de Gerenciamento de Contatos",
        add_completion=False,
        no_args_is_help=False,
    )

    def limpar_tela():
        """Limpa a tela do terminal de forma confiavel."""
        os.system("cls" if platform.system() == "Windows" else "clear")

    @app.command()
    def adicionar():
        """
        Adiciona um novo contato atraves de um formulario interativo.
        """
        limpar_tela()
        console.print(Panel.fit("[bold cyan]Adicionar Novo Contato[/bold cyan]", border_style="cyan", padding=(0, 2)))

        nome = Prompt.ask("[bold cyan]Nome completo[/bold cyan]")
        if not nome:
            console.print("[bold red]Erro:[/bold red] Nome e obrigatorio!")
            return

        data_nasc = Prompt.ask("[dim]Data de nascimento (DD/MM/AAAA)[/dim]", default="")
        email = Prompt.ask("[dim]Email[/dim]", default="")
        telefone = Prompt.ask("[dim]Telefone[/dim]", default="")
        endereco = Prompt.ask("[dim]Endereco[/dim]", default="")
        nome_pai = Prompt.ask("[dim]Nome do Pai[/dim]", default="")
        nome_mae = Prompt.ask("[dim]Nome da Mae[/dim]", default="")
        cpf = Prompt.ask("[dim]CPF[/dim]", default="")
        rg = Prompt.ask("[dim]RG[/dim]", default="")
        notas = Prompt.ask("[dim]Notas[/dim]", default="")

        console.print()
        if Confirm.ask("[bold]Salvar este contato?[/bold]"):
            sucesso, msg = controller.criar_contato(
                nome_completo=nome,
                data_nascimento=data_nasc,
                email=email,
                telefone=telefone,
                endereco=endereco,
                nome_pai=nome_pai,
                nome_mae=nome_mae,
                cpf=cpf,
                rg=rg,
                notas=notas,
            )

            if sucesso:
                console.print(f"[bold green]OK:[/bold green] {msg}")
            else:
                console.print(f"[bold red]Erro:[/bold red] {msg}")
        else:
            console.print("[yellow]Operacao cancelada.[/yellow]")

    @app.command()
    def listar():
        """
        Lista todos os contatos cadastrados em uma tabela formatada.
        """
        contatos = controller.obter_todos_contatos()

        if not contatos:
            console.print("[yellow]Nenhum contato encontrado.[/yellow]")
            return

        table = Table(title=f"Contatos ({len(contatos)})")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Nome", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Telefone", style="yellow")

        for contato in contatos:
            table.add_row(
                str(contato.id),
                contato.nome_completo,
                contato.email or "-",
                contato.telefone or "-",
            )

        console.print(table)

    @app.command()
    def buscar(termo: str):
        """
        Busca contatos por nome.
        """
        resultados = controller.buscar_contatos_por_nome(termo)

        if not resultados:
            console.print(f"[yellow]Nenhum contato encontrado com o termo '{termo}'.[/yellow]")
            return

        console.print(f"[bold]Encontrados {len(resultados)} resultados para '{termo}':[/bold]")

        for contato in resultados:
            console.print(Panel(
                f"[bold]ID:[/bold] {contato.id}\n"
                f"[bold]Email:[/bold] {contato.email}\n"
                f"[bold]Telefone:[/bold] {contato.telefone}\n"
                f"[bold]Endereco:[/bold] {contato.endereco}\n"
                f"[bold]Pai:[/bold] {contato.nome_pai}\n"
                f"[bold]Mae:[/bold] {contato.nome_mae}\n"
                f"[bold]CPF:[/bold] {contato.cpf}\n"
                f"[bold]RG:[/bold] {contato.rg}\n"
                f"[italic]{contato.notas}[/italic]",
                title=f"[bold cyan]{contato.nome_completo}[/bold cyan]",
                expand=False,
            ))

    @app.command()
    def modificar(id: int):
        """
        Modifica um contato existente.
        """
        contato = controller.obter_contato_por_id(id)

        if not contato:
            console.print(f"[bold red]Erro:[/bold red] Contato com ID {id} nao encontrado.")
            return

        console.print(Panel(f"Editando: [bold cyan]{contato.nome_completo}[/bold cyan]", border_style="yellow"))
        console.print("[italic]Pressione Enter para manter o valor atual[/italic]\n")

        novo_nome = Prompt.ask("Nome completo", default=contato.nome_completo)
        nova_data = Prompt.ask("Data de nascimento", default=contato.data_nascimento)
        novo_email = Prompt.ask("Email", default=contato.email)
        novo_telefone = Prompt.ask("Telefone", default=contato.telefone)
        novo_endereco = Prompt.ask("Endereco", default=contato.endereco)
        novo_nome_pai = Prompt.ask("Nome do Pai", default=contato.nome_pai)
        novo_nome_mae = Prompt.ask("Nome da Mae", default=contato.nome_mae)
        novo_cpf = Prompt.ask("CPF", default=contato.cpf)
        novo_rg = Prompt.ask("RG", default=contato.rg)
        novas_notas = Prompt.ask("Notas", default=contato.notas)

        if Confirm.ask("Salvar alteracoes?"):
            sucesso, msg = controller.modificar_contato(
                id,
                nome_completo=novo_nome,
                data_nascimento=nova_data,
                email=novo_email,
                telefone=novo_telefone,
                endereco=novo_endereco,
                nome_pai=novo_nome_pai,
                nome_mae=novo_nome_mae,
                cpf=novo_cpf,
                rg=novo_rg,
                notas=novas_notas,
            )

            if sucesso:
                console.print(f"[bold green]OK:[/bold green] {msg}")
            else:
                console.print(f"[bold red]Erro:[/bold red] {msg}")
        else:
            console.print("[yellow]Alteracoes descartadas.[/yellow]")

    @app.command()
    def remover(id: int):
        """
        Remove um contato pelo ID.
        """
        contato = controller.obter_contato_por_id(id)

        if not contato:
            console.print(f"[bold red]Erro:[/bold red] Contato com ID {id} nao encontrado.")
            return

        if Confirm.ask(f"Tem certeza que deseja remover [bold red]{contato.nome_completo}[/bold red]?"):
            sucesso, msg = controller.remover_contato(id)
            if sucesso:
                console.print(f"[bold green]OK:[/bold green] {msg}")
            else:
                console.print(f"[bold red]Erro:[/bold red] {msg}")

    @app.command()
    def exportar(formato: str = typer.Option("csv", help="Formato de exportacao: csv ou txt")):
        """
        Exporta todos os contatos para um arquivo.
        """
        formato = formato.lower()

        if formato not in ["csv", "txt"]:
            console.print(f"[bold red]Erro:[/bold red] Formato '{formato}' invalido. Use 'csv' ou 'txt'.")
            return

        if formato == "csv":
            sucesso, msg = controller.exportar_para_csv()
        else:
            sucesso, msg = controller.exportar_para_txt()

        if sucesso:
            console.print(f"[bold green]OK:[/bold green] {msg}")
        else:
            console.print(f"[bold red]Erro:[/bold red] {msg}")

    def executar_menu():
        def buscar_menu():
            termo = Prompt.ask("[bold]Digite o nome para buscar[/bold]")
            buscar(termo)

        def modificar_menu():
            id_str = Prompt.ask("[bold]ID do contato a modificar[/bold]")
            if id_str.isdigit():
                modificar(int(id_str))
            else:
                console.print("[red]ID invalido![/red]")

        def remover_menu():
            id_str = Prompt.ask("[bold]ID do contato a remover[/bold]")
            if id_str.isdigit():
                remover(int(id_str))
            else:
                console.print("[red]ID invalido![/red]")

        def exportar_menu():
            formato = Prompt.ask("[bold]Formato[/bold]", choices=["csv", "txt"], default="csv")
            exportar(formato)

        handlers = {
            "1": adicionar,
            "2": listar,
            "3": buscar_menu,
            "4": modificar_menu,
            "5": remover_menu,
            "6": exportar_menu,
        }
        menu_interativo(console, limpar_tela, handlers)

    @app.callback(invoke_without_command=True)
    def main(ctx: typer.Context):
        """
        Sistema de Gerenciamento de Contatos Pebbl_.

        Se nenhum comando for passado, abre o menu interativo.
        """
        if ctx.invoked_subcommand is None:
            executar_menu()

    return app
