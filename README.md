# Pebbl_ - Gerenciador de Contatos (CLI)

Pebbl_ é uma aplicação de linha de comando (CLI) em Python para gerenciar contatos. A interface usa `Typer` + `Rich` e a persistência, no estado atual do projeto, é feita via **Firebase Realtime Database** (veja `app/backend/controller/contato_controller.py`).

## Funcionalidades

- Adicionar, listar, buscar, modificar e remover contatos
- Exportar dados (CSV/TXT)
- Validações (CPF, RG, email, data)
- Logs em `logs/`

## Requisitos

- Python 3.x
- Dependências em `requirements.txt`
- Para executar com o backend padrão (Firebase):
  - `serviceAccountKey.json` na raiz do projeto
  - variável `FIREBASE_DATABASE_URL` definida (via `.env` ou variável de ambiente)

## Instalação

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuração Firebase

1. Crie/abra um projeto no Firebase Console e habilite **Realtime Database**
2. Baixe a chave de conta de serviço e salve como `serviceAccountKey.json` na raiz do projeto
3. Configure a URL do Realtime Database no `.env` (há um exemplo neste repositório):

```bash
FIREBASE_DATABASE_URL=https://projeto-exemplo.firebaseio.com
```

Guia passo-a-passo: `doc/firebase/FIREBASE_SETUP.md`.

## Como executar

Recomendado (carrega `.env` antes de iniciar a CLI):

```bash
python run.py
```

Ou comandos diretos do Typer:

```bash
python -m app.main adicionar
python -m app.main listar
python -m app.main buscar "Exemplo"
python -m app.main modificar 1
python -m app.main remover 1
python -m app.main exportar --formato csv
```

## Estrutura (resumo)

```
pebbl/
  app/
    main.py                             # CLI (Typer + Rich)
    backend/
      controller/contato_controller.py  # Orquestra as operações (usa Firebase)
      database/firebase_manager.py      # CRUD no Firebase Realtime Database
      database/firebase_config.py       # Helpers de configuração
      database/database_manager.py      # Persistência JSON (legado/não padrão)
      models/contato.py
      utils/{validators.py,logger.py}
  doc/firebase/                         # Documentação de setup do Firebase
  run.py                                # Entry-point (carrega .env e chama a CLI)
  requirements.txt
```

## Observações

- Credenciais e arquivos exportados não devem ir para o Git; confira `.gitignore`.
- Parte da documentação antiga ainda cita JSON local; a execução padrão atual utiliza Firebase.
