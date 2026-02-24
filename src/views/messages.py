###############################################################################
#  
#	FILE: 	messages.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	26 06 2025
#	WHAT:	Mensagens para tipos de ações
#
################################################################################

# Imports
from emoji import emojize

messages = {
    # Sucesso
    "SAVE_SUCCESS": emojize(":check_mark_button: - Dados salvos com sucesso!"),
    "UPDATE_SUCCESS": emojize(":check_mark_button: - Dados atualizados com sucesso!"),
    "DELETE_SUCCESS": emojize(":wastebasket: - Item deletado com sucesso."),
    "LOGIN_SUCCESS": emojize(":locked_with_key: - Login efetuado com sucesso!"),
    
    # Erro
    "SAVE_ERROR": emojize(":cross_mark: - Erro ao salvar os dados."),
    "UPDATE_ERROR": emojize(":cross_mark: - Erro ao atualizar os dados."),
    "DELETE_ERROR": emojize(":cross_mark: - Erro ao deletar o item."),
    "LOGIN_FAILED": emojize(":no_entry: - Falha no login. Verifique suas credenciais."),
    "UNEXPECTED_ERROR": emojize(":warning: - \033[1;33;40mOcorreu um erro inesperado.\033[m"),
    
    # Avisos / Alertas
    "INVALID_INPUT": emojize(":warning: - \033[1;31;40mENTRADA INVÁLIDA! Por favor, tente novamente!\033[m"),
    "FIELD_REQUIRED": emojize(":warning: - O campo '{field}' é obrigatório."),
    "ACTION_UNAVAILABLE": emojize(":warning: - Ação indisponível no momento."),
    
    # Informações
    "LOADING": emojize(":hourglass_not_done: - Carregando..."),
    "PLEASE_WAIT": emojize(":counterclockwise_arrows_button: - Por favor, aguarde..."),
    "NO_RESULTS": emojize(":magnifying_glass_tilted_left: - Nenhum resultado encontrado."),
    "WELCOME": emojize(":sparkles: - Bem-vindo(a), {name}!"),
    
    # Confirmações
    "CONFIRM_DELETE": emojize(":warning: - Tem certeza que deseja excluir este item?"),
    "CONFIRM_LOGOUT": emojize(":door: - Deseja realmente sair da conta?"),

    # Outros
    "SESSION_EXPIRED": emojize(":hourglass_done: - Sessão expirada. Faça login novamente."),
    "PERMISSION_DENIED": emojize(":no_entry: - Você não tem permissão para essa ação."),
}
