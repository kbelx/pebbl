# Pebbl_ - Sistema de Gerenciamento de Contatos

## Visão Geral

**Pebbl_** é uma aplicação de linha de comando (CLI) moderna para gerenciar contatos pessoais de forma intuitiva e eficiente. Desenvolvida com Python, utiliza a biblioteca `Typer` para interface CLI e `Rich` para formatação avançada de texto e tabelas no terminal.

### Características Principais

- ✅ Adicionar, listar, buscar, modificar e remover contatos
- ✅ Armazenamento em JSON local (sem dependências de banco de dados externo)
- ✅ Validação automática de dados (CPF, RG, Email, Data)
- ✅ Interface interativa com menu navegável
- ✅ Exportação para CSV e TXT
- ✅ Logs detalhados de operações
- ✅ Suporte a múltiplos campos por contato (nome, CPF, RG, dados parentais, etc.)

---

## Arquitetura

O projeto segue a arquitetura em **3 camadas**:

```
┌─────────────────────────────────────┐
│   Frontend (main.py)                 │
│   - CLI com Typer e Rich            │
│   - Menu Interativo                 │
├─────────────────────────────────────┤
│   Backend Controller                 │
│   - Lógica de Negócio               │
│   - Validações                      │
├─────────────────────────────────────┤
│   Database Manager                   │
│   - Operações CRUD                  │
│   - Persistência em JSON            │
└─────────────────────────────────────┘
```

---

## Telas da Aplicação

### **Tela Principal - Menu Interativo**

```
╔════════════════════════════════════╗
║  PEBBL_ - Menu Principal           ║
╚════════════════════════════════════╝

[1] Adicionar novo contato
[2] Listar todos os contatos
[3] Buscar contato
[4] Modificar contato
[5] Remover contato
[6] Exportar dados
[0] Sair

Escolha uma opção: _
```

---

### **Adicionar Novo Contato**

```
╔════════════════════════════════════╗
║  Adicionar Novo Contato            ║
╚════════════════════════════════════╝

Nome completo: João da Silva
Data de nascimento (DD/MM/AAAA): 25/08/1990
Email: joao.silva@exemplo.com
Telefone: (00) 00000-0000
Endereço: Rua das Flores, 123
Nome do Pai: José Silva
Nome da Mãe: Maria Silva
CPF: 123.456.789-00
RG: 12.345.678-9
Notas: Amigo da faculdade

Salvar este contato? [Y/n]: y

✓ Contato 'João da Silva' adicionado com sucesso! (ID: 1)

Pressione Enter para voltar ao menu
```

---

### **Listar Todos os Contatos**

```
Contatos (3)
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ ID ┃ Nome           ┃ Email           ┃ Telefone     ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1  │ João da Silva  │ joao@ex.com     │ (11) 98765-  │
│ 2  │ Maria Santos   │ maria@ex.com    │ (11) 99876-  │
│ 3  │ Pedro Oliveira │ pedro@ex.com    │ (21) 97654-  │
└────┴────────────────┴─────────────────┴──────────────┘

Pressione Enter para voltar ao menu
```

---

### **Buscar Contato por Nome**

```
Digite o nome para buscar: João

Encontrados 1 resultados para 'João':

╔════════════════════════════════════════╗
║     João da Silva                      ║
╠════════════════════════════════════════╣
║ ID: 1                                  ║
║ Email: joao.silva@exemplo.com         ║
║ Telefone: (00) 00000-0000             ║
║ Endereço: Rua das Flores, 123         ║
║ Pai: José Silva                        ║
║ Mãe: Maria Silva                       ║
║ CPF: 123.456.789-00                    ║
║ RG: 12.345.678-9                       ║
║ Amigo da faculdade. Gosta de tech.    ║
╚════════════════════════════════════════╝

Pressione Enter para voltar ao menu
```

---

### **Modificar Contato**

```
ID do contato a modificar: 1

╔════════════════════════════════════╗
║  Editando: João da Silva           ║
╚════════════════════════════════════╝

Pressione Enter para manter o valor atual

Nome completo [João da Silva]: Contato Exemplo Oliveira
Data de nascimento [25/08/1990]: 
Telefone [(00) 00000-0000]: (11) 99999-9999
Email [joao.silva@exemplo.com]: 

Salvar alterações? [Y/n]: y

✓ Contato atualizado com sucesso!

Pressione Enter para voltar ao menu
```

---

### **Remover Contato**

```
ID do contato a remover: 1

Tem certeza que deseja remover João da Silva? [Y/n]: y

✓ Contato removido com sucesso!

Pressione Enter para voltar ao menu
```

---

### **Exportar Dados**

```
Formato de exportação (csv ou txt) [csv]: csv

✓ Dados exportados com sucesso para 'contatos.csv'!
```

Gera arquivos com os seguintes formatos:

**CSV:**
```
id,nome_completo,email,telefone,cpf,rg,data_nascimento
1,João da Silva,joao.silva@exemplo.com,(00) 00000-0000,123.456.789-00,12.345.678-9,25/08/1990
```

**TXT:**
```
===== CONTATOS EXPORTADOS =====
Data: 19/11/2025 - 14:35:20

ID: 1
Nome: João da Silva
Email: joao.silva@exemplo.com
Telefone: (00) 00000-0000
CPF: 123.456.789-00
RG: 12.345.678-9
...
```

---

## Campos do Contato

Cada contato possui os seguintes campos:

| Campo | Tipo | Validação | Obrigatório |
|-------|------|-----------|------------|
| ID | int | Auto-gerado | ✓ |
| Nome Completo | string | Min 3 caracteres | ✓ |
| Email | string | Validação de email | ✗ |
| Telefone | string | Formato livre | ✗ |
| CPF | string | Validação de CPF | ✗ |
| RG | string | Formato livre | ✗ |
| Data de Nascimento | string | DD/MM/AAAA | ✗ |
| Endereço | string | Formato livre | ✗ |
| Nome do Pai | string | Formato livre | ✗ |
| Nome da Mãe | string | Formato livre | ✗ |
| Notas | string | Formato livre | ✗ |
| Data de Criação | datetime | Auto-gerada | ✓ |
| Data de Modificação | datetime | Auto-gerada | ✓ |

---

## Como Usar

### Instalação

```bash
# 1. Navegar até o diretório do projeto
cd pebbl

# 2. Criar um ambiente virtual
python -m venv env

# 3. Ativar o ambiente virtual
# No Windows:
env\Scripts\activate
# No Linux/Mac:
source env/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt
```

### Executar a Aplicação

```bash
python run.py
```

Ou use os comandos diretos do Typer:

```bash
python -m app.main adicionar
python -m app.main listar
python -m app.main buscar "Exemplo"
python -m app.main modificar 1
python -m app.main remover 1
python -m app.main exportar --formato csv
```

---

## Estrutura de Pastas

```
pebbl/
├── app/
│   ├── main.py                      # Ponto de entrada (CLI com Typer)
│   ├── backend/
│   │   ├── controller/
│   │   │   └── contato_controller.py   # Lógica de negócio
│   │   ├── database/
│   │   │   ├── database_manager.py     # CRUD e persistência
│   │   │   └── data/
│   │   │       └── contatos.json       # Arquivo de dados
│   │   ├── models/
│   │   │   └── contato.py              # Modelo de dados
│   │   └── utils/
│   │       ├── validators.py           # Validações (CPF, Email, etc)
│   │       └── logger.py               # Sistema de logs
│   └── frontend/
│       └── utils/
│           └── messages.py             # Mensagens da aplicação
├── run.py                           # Script de inicialização
├── requirements.txt                 # Dependências do projeto
└── doc/
    ├── README.md                    # Este arquivo
    ├── API.md                       # Documentação da API
    └── diagrams/                    # Diagramas UML e fluxos
```

---

## Dependências

- **typer**: Framework para CLI
- **rich**: Formatação avançada de texto e tabelas
- **click**: Lib de utilidades para CLI (dependência do Typer)
- **colorama**: Suporte a cores no terminal

---

## Funcionalidades Implementadas

✅ **CRUD Completo**
- Criar, ler, atualizar e deletar contatos

✅ **Busca e Filtro**
- Buscar por nome

✅ **Exportação**
- CSV e TXT

✅ **Validação de Dados**
- CPF, RG, Email, Data

✅ **Persistência**
- Armazenamento em JSON

✅ **Interface Amigável**
- Menu interativo com Rich
- Painéis, tabelas e formatação visual

✅ **Sistema de Logs**
- Logs de operações para debug

---

## Futuros Melhoramentos

- [ ] Busca avançada (por email, CPF, telefone)
- [ ] Importação de dados (CSV, JSON)
- [ ] Sincronização em nuvem
- [ ] Backup automático
- [ ] Interface gráfica (GUI)
- [ ] Autenticação e usuários
- [ ] Banco de dados SQL (SQLite/PostgreSQL)