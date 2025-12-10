# 🔥 Firebase Integration Guide

## ✅ Pré-requisitos

1. **Conta Google** (gratuita)
2. **Acesso ao Firebase Console** (https://console.firebase.google.com)

---

## 🚀 Passo 1: Criar Projeto no Firebase

1. Acesse [Firebase Console](https://console.firebase.google.com)
2. Clique em **"Criar projeto"**
3. Digite o nome do projeto: `pebbl`
4. Clique em **"Continuar"**
5. Desabilite Google Analytics (opcional)
6. Clique em **"Criar projeto"**

---

## 🔑 Passo 2: Baixar Credenciais

1. No Firebase Console, vá para **⚙️ Configurações do Projeto**
2. Clique na aba **"Contas de Serviço"**
3. Clique em **"Gerar nova chave privada"**
4. Salve o arquivo `serviceAccountKey.json` na **raiz do projeto**
   ```
   pebbl/
   ├── serviceAccountKey.json  ← AQUI
   ├── requirements.txt
   ├── run.py
   ├── app/
   └── ...
   ```

⚠️ **IMPORTANTE**: Nunca commit este arquivo no Git! Já está no `.gitignore`.

---

## 📊 Passo 3: Criar Banco de Dados Realtime

1. No Firebase Console, vá para **Realtime Database** (menu esquerdo)
2. Clique em **"Criar banco de dados"**
3. Escolha a região: **`us-central1`** (padrão)
4. Escolha modo de segurança: **"Iniciar no modo de teste"** (por enquanto)
5. Clique em **"Ativar"**

Você verá uma URL como:
```
https://projeto-exemplo.firebaseio.com
```

---

## 🌍 Passo 4: Configurar Variável de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
FIREBASE_DATABASE_URL=https://projeto-exemplo.firebaseio.com
```

Ou configure no PowerShell:

```powershell
$env:FIREBASE_DATABASE_URL="https://projeto-exemplo.firebaseio.com"
```

---

## 📦 Passo 5: Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## 🔄 Passo 6: Usar FirebaseManager

### Opção A: Mudar o Controller para usar Firebase

**Antes (JSON):**
```python
from backend.database.database_manager import DatabaseManager
db = DatabaseManager()
```

**Depois (Firebase):**
```python
from backend.database.firebase_manager import FirebaseManager
db = FirebaseManager()
```

**Vantagem**: O resto do código permanece idêntico! 🎯

### Exemplo Completo:

```python
from backend.database.firebase_manager import FirebaseManager
from backend.models.contato import Contato

# Inicializa conexão (primeira vez é mais lenta)
db = FirebaseManager()

# Adicionar contato
novo_contato = Contato(
    nome_completo="Contato Exemplo",
    email="contato@exemplo.com",
    telefone="00000000000"
)
sucesso, msg = db.adicionar_contato(novo_contato)
print(msg)

# Listar contatos
contatos = db.listar_contatos()
for c in contatos:
    print(f"{c.nome_completo} - {c.email}")

# Buscar contato
encontrado = db.buscar_por_nome("Exemplo")

# Deletar contato
sucesso, msg = db.deletar_contato(1)
```

---

## 🛡️ Passo 7: Configurar Segurança (Importante!)

⚠️ **Modo de teste expira em 30 dias!**

### Para produção, acesse Firebase Console:

1. **Realtime Database** → **Regras**
2. Configure para autenticação:

```json
{
  "rules": {
    "pebbl": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

3. Clique em **"Publicar"**

---

## ✨ Benefícios do Firebase

| Feature | JSON | Firebase |
|---------|------|----------|
| Banco Online | ❌ | ✅ |
| Sync Automático | ❌ | ✅ |
| Autenticação | ❌ | ✅ |
| Backup Automático | ❌ | ✅ |
| Plano Gratuito | ✅ | ✅ (generoso) |
| Infraestrutura | Você | Google |

---

## 🐛 Troubleshooting

### Erro: "serviceAccountKey.json not found"
```
Solução: Baixe novamente o arquivo e coloque na raiz do projeto
```

### Erro: "FIREBASE_DATABASE_URL not defined"
```
Solução: Configure a variável de ambiente com a URL do seu BD
```

### Erro: "Permission denied"
```
Solução: Mude as regras do Firebase para modo teste (temporário)
```

---

## 📚 Próximos Passos

1. **Autenticação**: Adicionar login com email/senha
2. **Backup**: Implementar exportação automática para JSON
3. **Sincronização**: Sincronizar offline-first com dados online
4. **Análise**: Usar Firebase Analytics para rastrear uso

---

## 📞 Referências

- [Firebase Docs](https://firebase.google.com/docs)
- [Realtime Database Guide](https://firebase.google.com/docs/database)
- [Python Admin SDK](https://firebase.google.com/docs/database/admin/start)
