import typer

# importações Rich
from rich.prompt import Prompt

# Importações do Projeto
from src.views.menu import menu_interativo
from src.views.utils.formatter import limpar_tela

# importações do CLI
from src.views.cli.adicionar import adicionar
from src.views.cli.listar import listar
from src.views.cli.buscar import buscar
from src.views.cli.modificar import modificar
from src.views.cli.remover import remover
from src.views.cli.exportar import exportar

def build_app(controller, console):
    app = typer.Typer(
        help="Pebbl_ - Sistema de Gerenciamento de Contatos",
        add_completion=False,
        no_args_is_help=False,
    )

    @app.command("adicionar")
    def adicionar_cmd():
        """Adiciona um novo contato."""
        adicionar(controller, console)

    @app.command("listar")
    def listar_cmd():
        """Lista todos os contatos."""
        listar(controller, console)

    @app.command("buscar")
    def buscar_cmd(termo: str):
        """Busca contatos por nome."""
        buscar(controller, console, termo)

    @app.command("modificar")
    def modificar_cmd(id: int):
        """Modifica um contato existente pelo ID."""
        modificar(controller, console, id)

    @app.command("remover")
    def remover_cmd(id: int):
        """Remove um contato pelo ID."""
        remover(controller, console, id)

    @app.command("exportar")
    def exportar_cmd(formato: str = typer.Option("csv", help="Formato de exportacao: csv ou txt")):
        """Exporta todos os contatos para um arquivo."""
        exportar(controller, console, formato)


    def executar_menu():
        def buscar_menu():
            termo = Prompt.ask("[bold]Digite o nome para buscar[/bold]")
            buscar(controller, console, termo)

        def modificar_menu():
            id_str = Prompt.ask("[bold]ID do contato a modificar[/bold]")
            if id_str.isdigit():
                modificar(controller, console, int(id_str))
            else:
                console.print("[red]ID invalido![/red]")

        def remover_menu():
            id_str = Prompt.ask("[bold]ID do contato a remover[/bold]")
            if id_str.isdigit():
                remover(controller, console, int(id_str))
            else:
                console.print("[red]ID invalido![/red]")

        def exportar_menu():
            formato = Prompt.ask("[bold]Formato[/bold]", choices=["csv", "txt"], default="csv")
            exportar(controller, console, formato)

        handlers = {
            "1": lambda: adicionar(controller, console),
            "2": lambda: listar(controller, console),
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
