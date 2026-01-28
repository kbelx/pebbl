# Pebbl_ - Gerenciador de Contatos (CLI)

Pebbl_ e uma aplicacao de linha de comando (CLI) em Python para gerenciar contatos. A interface usa `Typer` + `Rich` e a persistencia, no estado atual do projeto, e feita via **Firebase Realtime Database** (veja `app/backend/controller/contato_controller.py`).

## Funcionalidades

- Adicionar, listar, buscar, modificar e remover contatos
- Exportar dados (CSV/TXT)
- Validacoes (CPF, RG, email, data)
- Logs em `logs/`
- Menu interativo no terminal

## Requisitos

- Python 3.x
- Dependencias em `requirements.txt`
- Para executar com o backend padrao (Firebase):
  - `serviceAccountKey.json` na raiz do projeto
  - variavel `FIREBASE_DATABASE_URL` definida (via `.env` ou variavel de ambiente)

## Instalacao

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuracao Firebase

1. Crie/abra um projeto no Firebase Console e habilite **Realtime Database**
2. Baixe a chave de conta de servico e salve como `serviceAccountKey.json` na raiz do projeto
3. Configure a URL do Realtime Database no `.env` (ha um exemplo neste repositorio):

```bash
FIREBASE_DATABASE_URL=https://projeto-exemplo.firebaseio.com
```

Guia passo-a-passo: `doc/firebase/FIREBASE_SETUP.md`.

## Como executar

Recomendado (carrega `.env` antes de iniciar a aplicacao):

```bash
python run.py
```

Comandos diretos (Typer):

```bash
python run.py listar
python run.py buscar "Exemplo"
python run.py modificar 1
python run.py remover 1
python run.py exportar --formato csv
```

Alternativa equivalente:

```bash
python -m app.main listar
python -m app.main buscar "Exemplo"
```

Observacao: a interface grafica foi removida. `python run.py gui` encerra com uma mensagem informativa.

## Estrutura (resumo)

```
pebbl/
  app/
    main.py                             # Orquestracao do app (Typer)
    frontend/
      cli.py                            # UI CLI (Typer + Rich)
      menu.py                           # Menu interativo
    backend/
      controller/contato_controller.py  # Orquestra as operacoes (usa Firebase)
      database/firebase_manager.py      # CRUD no Firebase Realtime Database
      database/firebase_config.py       # Helpers de configuracao
      database/database_manager.py      # Persistencia JSON (legado/nao padrao)
      models/contato.py
      utils/{validators.py,logger.py}
  doc/firebase/                         # Documentacao de setup do Firebase
  run.py                                # Entry-point (carrega .env e chama a CLI)
  requirements.txt
```

## Observacoes

- Credenciais e arquivos exportados nao devem ir para o Git; confira `.gitignore`.
- Parte da documentacao antiga ainda cita JSON local; a execucao padrao atual utiliza Firebase.
