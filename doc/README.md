Em um projeto de interface de linha de comando (CLI), as telas são representadas por texto puro. Elas funcionam como menus interativos onde o usuário digita comandos ou opções.

Abaixo estão exemplos de como as telas para cada função do seu aplicativo pessoal "Pebbl\_" ficariam, com base no diagrama de caso de uso e no foco em dados de pessoas.

-----

### **Tela Principal**

Esta seria a primeira tela, o "menu" principal do aplicativo, onde o usuário pode escolher a ação que deseja realizar.

```
Bem-vindo ao Pebbl_!
Escolha uma opção:

1. Adicionar dados
2. Consultar dados
3. Modificar dados
4. Exportar dados
5. Remover dados
6. Sair

> _
```

-----

### **Tela de Adicionar Dados**

Quando o usuário seleciona a opção **1**, esta tela aparece para coletar as informações de um novo contato.

```
--- Adicionar novo contato ---

Nome completo:
> João da Silva

Data de nascimento (DD/MM/AAAA):
> 25/08/1990

Email:
> joao.silva@exemplo.com

Telefone:
> (00) 00000-0000

Endereço:
> Rua das Flores, 123

Notas (opcional):
> Amigo da faculdade. Gosta de tecnologia.

Contato adicionado com sucesso!
Pressione ENTER para voltar ao menu.
```

-----

### **Tela de Consultar Dados**

Ao escolher a opção **2**, o usuário é levado a um menu de busca.

```
--- Consultar dados ---

Como deseja buscar?

1. Por nome
2. Por email
3. Listar todos
4. Voltar

> 1

Digite o nome a ser buscado:
> João

--- Resultados ---
Nome: João da Silva
Data de nascimento: 25/08/1990
Email: joao.silva@exemplo.com
Telefone: (00) 00000-0000

Pressione ENTER para voltar.
```

-----

### **Tela de Modificar Dados**

Na opção **3**, o usuário primeiro busca o contato que deseja modificar e, em seguida, escolhe qual informação alterar.

```
--- Modificar dados ---

Digite o nome do contato que deseja modificar:
> João da Silva

O que deseja modificar?

1. Telefone
2. Email
3. Endereço
4. Notas
5. Voltar

> 1

Digite o novo telefone:
> (11) 99887-7665

Telefone atualizado com sucesso!
Pressione ENTER para voltar ao menu.
```

-----

### **Tela de Exportar Dados**

A opção **4** apresenta as opções de formato para exportação.

```
--- Exportar dados ---

Em qual formato deseja exportar?

1. Planilha (CSV)
2. Texto (TXT)
3. Voltar

> 1

Dados exportados com sucesso para "contatos.csv"!
Pressione ENTER para voltar ao menu.
```

-----

### **Tela de Remover Dados**

Ao escolher a opção **5**, o aplicativo pede uma confirmação para evitar exclusões acidentais.

```
--- Remover dados ---

Digite o nome do contato que deseja remover:
> João da Silva

Tem certeza que deseja remover João da Silva? (S/N)
> S

Contato removido com sucesso.
Pressione ENTER para voltar ao menu.
```