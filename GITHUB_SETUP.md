# 🚀 Guia para Subir o Projeto no GitHub

## Pré-requisitos

1. **Git instalado**: Verifique se o Git está instalado
   ```bash
   git --version
   ```

2. **Conta no GitHub**: Crie uma conta em https://github.com se ainda não tiver

## Passo a Passo

### 1. Inicializar o repositório Git (se ainda não foi feito)

```bash
git init
```

### 2. Adicionar todos os arquivos

```bash
git add .
```

### 3. Fazer o primeiro commit

```bash
git commit -m "Initial commit: Sistema de IA para Coup com aprendizado persistente"
```

### 4. Criar repositório no GitHub

1. Acesse https://github.com
2. Clique em **"+"** no canto superior direito → **"New repository"**
3. Escolha um nome para o repositório (ex: `coup-ai-assistant`)
4. **NÃO** marque "Initialize with README" (já temos README)
5. Clique em **"Create repository"**

### 5. Conectar ao repositório remoto

**IMPORTANTE**: Substitua `SEU_USUARIO` pelo seu username do GitHub e `NOME_DO_REPOSITORIO` pelo nome que você escolheu.

```bash
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
```

Exemplo:
```bash
git remote add origin https://github.com/rykel/coup-ai-assistant.git
```

### 6. Renomear branch para main (se necessário)

```bash
git branch -M main
```

### 7. Enviar para o GitHub

```bash
git push -u origin main
```

Se pedir credenciais:
- **Username**: Seu username do GitHub
- **Password**: Use um **Personal Access Token** (não a senha normal)
  - Para criar: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Marque a opção `repo`
  - Copie o token e use como senha

## ✅ Pronto!

Seu projeto está no GitHub! Você pode verificar em:
`https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO`

## 📝 Próximas Atualizações

Para enviar futuras mudanças:

```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

## 🔒 Arquivos Protegidos

Os seguintes arquivos **NÃO** serão enviados (estão no .gitignore):
- `venv/` - Ambiente virtual
- `.env` - Variáveis de ambiente (chaves API)
- `ai_learning.json` - Dados de treinamento pessoais
- `__pycache__/` - Cache do Python

## ⚠️ Importante

1. **Nunca commite chaves API** - Use arquivo `.env` (já está no .gitignore)
2. **Não commite o arquivo de aprendizado** - É pessoal e pode ser grande
3. **Verifique antes de fazer push** - Use `git status` para ver o que será enviado

