###############################################################################
#  
#	FILE: 	modificar.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	Modifica algum dado da base de dados
#
################################################################################

from rich.panel import Panel
from rich.prompt import Prompt, Confirm


def modificar(controller, console, id: int):
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
