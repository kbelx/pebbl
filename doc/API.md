# Pebbl_ - Documentação da API

## Visão Geral

Pebbl_ é um sistema de gerenciamento de contatos CLI moderno desenvolvido em Python com Rich e Typer.

## Estrutura do Projeto

```
pebbl/
├── app/
│   ├── backend/
│   │   ├── controller/      # Camada de negócio
│   │   ├── database/        # Camada de persistência
│   │   ├── models/          # Modelos de dados
│   │   └── utils/           # Utilitários
│   ├── frontend/            # Componentes da UI
│   └── main.py              # Entrada da aplicação
├── test/                    # Testes automatizados
├── doc/                     # Documentação
└── requirements.txt         # Dependências
```

## Camadas da Aplicação

### 1. Models (app/backend/models/)

**Contato** - Modelo de dados para contatos

```python
from backend.models.contato import Contato

contato = Contato(
    nome_completo="Contato Exemplo",
    email="contato@exemplo.com",
    telefone="00000000000",
    data_nascimento="15/03/1990",
    cpf="00000000000",
    rg="000000000"
)

# Validar dados
valido, mensagem = contato.validar()

# Converter para dicionário
dict_contato = contato.to_dict()

# Criar a partir de dicionário
novo_contato = Contato.from_dict(dict_contato)
```

### 2. Database (app/backend/database/)

**DatabaseManager** - Gerencia persistência em JSON

```python
from backend.database.database_manager import DatabaseManager

db = DatabaseManager()  # Usa caminho padrão

# Criar
sucesso, msg = db.adicionar_contato(contato)

# Listar
contatos = db.listar_todos()

# Buscar
contato = db.buscar_por_id(1)
contatos = db.buscar_por_nome("Exemplo")
contato = db.buscar_por_email("contato@exemplo.com")

# Atualizar
sucesso, msg = db.atualizar_contato(1, {"email": "atualizado@exemplo.com"})

# Remover
sucesso, msg = db.remover_contato(1)

# Exportar
sucesso, msg = db.exportar_csv("contatos.csv")
sucesso, msg = db.exportar_txt("contatos.txt")

# Estatísticas
stats = db.estatisticas()  # {"total": 1, "com_email": 1, ...}
```

### 3. Controller (app/backend/controller/)

**ContatoController** - Lógica de negócio e validações

```python
from backend.controller.contato_controller import ContatoController

controller = ContatoController()

# Criar contato
sucesso, msg = controller.criar_contato(
    nome_completo="Contato Exemplo",
    email="contato@exemplo.com",
    telefone="00000000000"
)

# Obter contatos
contatos = controller.obter_todos_contatos()
contato = controller.obter_contato_por_id(1)
resultados = controller.buscar_contatos_por_nome("Exemplo")

# Modificar
sucesso, msg = controller.modificar_contato(1, email="atualizado@exemplo.com")

# Remover
sucesso, msg = controller.remover_contato(1)

# Exportar
sucesso, msg = controller.exportar_para_csv()
sucesso, msg = controller.exportar_para_txt()

# Estatísticas
total = controller.contar_contatos()
stats = controller.obter_estatisticas()
```

### 4. Utilitários (app/backend/utils/)

**validators.py** - Funções de validação

```python
from backend.utils.validators import (
    validar_cpf,
    validar_rg,
    validar_email,
    validar_telefone,
    validar_data,
    sanitizar_texto
)

# Validar CPF
if validar_cpf("00000000000"):
    print("CPF válido")

# Validar Email
if validar_email("usuario@exemplo.com"):
    print("Email válido")

# Validar Telefone
if validar_telefone("(00) 00000-0000"):
    print("Telefone válido")

# Validar Data
valido, msg = validar_data("15/03/1990")

# Sanitizar
texto_limpo = sanitizar_texto("  texto   com   espaços  ")
```

**logger.py** - Sistema de logging

```python
from backend.utils.logger import Logger

logger = Logger.obter_logger("pebbl.modulo")

logger.debug("Mensagem de debug")
logger.info("Operação bem-sucedida")
logger.warning("Aviso: algo pode estar errado")
logger.error("Erro: operação falhou")
```

## Interface CLI (app/main.py)

### Comandos Disponíveis

```bash
# Menu interativo (sem argumentos)
python app/main.py

# Adicionar contato
python app/main.py adicionar

# Listar todos
python app/main.py listar

# Buscar por nome
python app/main.py buscar "Exemplo"

# Modificar contato
python app/main.py modificar 1

# Remover contato
python app/main.py remover 1

# Exportar dados
python app/main.py exportar --formato csv
python app/main.py exportar --formato txt
```

## Testes

```bash
# Executar testes de integração
python -m pytest test/test_integration.py -v

# Executar todos os testes
python -m pytest test/ -v

# Executar com cobertura
python -m pytest test/ --cov=app
```

## Estrutura de Dados - Contato

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | int | Sim | Identificador único (gerado automaticamente) |
| nome_completo | str | Sim | Nome completo (mín. 3, máx. 150 caracteres) |
| data_nascimento | str | Não | Formato DD/MM/AAAA |
| email | str | Não | Validado como email |
| telefone | str | Não | 10-13 dígitos |
| endereco | str | Não | Endereço completo |
| nome_pai | str | Não | Nome do pai |
| nome_mae | str | Não | Nome da mãe |
| cpf | str | Não | Validado com algoritmo oficial |
| rg | str | Não | 5-15 caracteres alfanuméricos |
| notas | str | Não | Anotações adicionais |
| data_criacao | str | Sim | ISO 8601 timestamp (automático) |
| data_modificacao | str | Sim | ISO 8601 timestamp (automático) |

## Tratamento de Erros

Todas as operações retornam tuplas `(sucesso: bool, mensagem: str)`:

```python
sucesso, msg = controller.criar_contato(...)

if sucesso:
    print(f"✓ {msg}")
else:
    print(f"✗ {msg}")
```

## Persistência

Os dados são armazenados em `app/backend/database/data/contatos.json`:

```json
{
  "versao": "1.0",
  "ultimo_id": 1,
  "contatos": [
    {
      "id": 1,
      "nome_completo": "Contato Exemplo",
      "email": "contato@exemplo.com",
      ...
    }
  ]
}
```

## Logging

Logs são salvos em `logs/pebbl_YYYYMMDD.log`:

- **DEBUG**: Operações internas e carregamento de dados
- **INFO**: Operações bem-sucedidas
- **WARNING**: Validações falhadas, tentativas inválidas
- **ERROR**: Exceções e falhas críticas

## Dependências

```
typer==0.9.0       # Framework CLI
rich==13.7.0       # Formatação de saída
click==8.1.7       # Complemento CLI
emoji==2.14.1      # Suporte a emojis
```

## Próximos Passos

- [ ] Adicionar autenticação de usuários
- [ ] Suportar múltiplos formatos de exportação (JSON, XML)
- [ ] Integração com banco de dados SQL
- [ ] API REST para acesso remoto
- [ ] Sincronização em nuvem
- [ ] Interface web

## Suporte

Para reportar bugs ou sugerir melhorias, abra uma issue no repositório.

---

**Projeto Pebbl_** - Sistema de Gerenciamento de Contatos  
Desenvolvido em: 18 de Novembro de 2025
