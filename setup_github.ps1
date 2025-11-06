# Script para configurar e enviar projeto para GitHub
# Execute: .\setup_github.ps1

Write-Host "🚀 Configurando repositório Git..." -ForegroundColor Cyan

# Verifica se Git está instalado
try {
    git --version | Out-Null
    Write-Host "✅ Git encontrado!" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não está instalado. Instale em: https://git-scm.com" -ForegroundColor Red
    exit
}

# Inicializa repositório se não existir
if (-not (Test-Path .git)) {
    Write-Host "📦 Inicializando repositório Git..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repositório inicializado!" -ForegroundColor Green
} else {
    Write-Host "✅ Repositório Git já existe!" -ForegroundColor Green
}

# Mostra status
Write-Host "`n📊 Status atual do repositório:" -ForegroundColor Cyan
git status

Write-Host "`n⚠️  ATENÇÃO: Antes de continuar:" -ForegroundColor Yellow
Write-Host "1. Crie um repositório no GitHub (https://github.com/new)" -ForegroundColor White
Write-Host "2. NÃO marque 'Initialize with README'" -ForegroundColor White
Write-Host "3. Anote o nome do repositório e seu username" -ForegroundColor White

$continue = Read-Host "`nJá criou o repositório no GitHub? (s/n)"

if ($continue -ne "s" -and $continue -ne "S") {
    Write-Host "`n📝 Passos para criar o repositório:" -ForegroundColor Cyan
    Write-Host "1. Acesse: https://github.com/new" -ForegroundColor White
    Write-Host "2. Escolha um nome (ex: coup-ai-assistant)" -ForegroundColor White
    Write-Host "3. Deixe em 'Public' ou 'Private'" -ForegroundColor White
    Write-Host "4. NÃO marque 'Initialize with README'" -ForegroundColor White
    Write-Host "5. Clique em 'Create repository'" -ForegroundColor White
    Write-Host "`nExecute este script novamente após criar o repositório." -ForegroundColor Yellow
    exit
}

# Pede informações
$username = Read-Host "`nDigite seu username do GitHub"
$repoName = Read-Host "Digite o nome do repositório"

# Adiciona todos os arquivos
Write-Host "`n📦 Adicionando arquivos..." -ForegroundColor Yellow
git add .

# Faz commit
$commitMsg = Read-Host "`nDigite a mensagem do commit (ou Enter para usar padrão)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Initial commit: Sistema de IA para Coup com aprendizado persistente"
}

Write-Host "💾 Fazendo commit..." -ForegroundColor Yellow
git commit -m $commitMsg

# Renomeia branch para main
Write-Host "🌿 Renomeando branch para main..." -ForegroundColor Yellow
git branch -M main

# Adiciona remote
Write-Host "🔗 Conectando ao GitHub..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$username/$repoName.git"

# Remove remote se já existir
git remote remove origin 2>$null

git remote add origin $remoteUrl
Write-Host "✅ Remote configurado: $remoteUrl" -ForegroundColor Green

# Verifica remote
Write-Host "`n📡 Remote configurado:" -ForegroundColor Cyan
git remote -v

Write-Host "`n🚀 Enviando para o GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  Se pedir credenciais:" -ForegroundColor Yellow
Write-Host "   - Username: $username" -ForegroundColor White
Write-Host "   - Password: Use Personal Access Token (não sua senha!)" -ForegroundColor White
Write-Host "   - Criar token: https://github.com/settings/tokens" -ForegroundColor White

$push = Read-Host "`nDeseja fazer push agora? (s/n)"

if ($push -eq "s" -or $push -eq "S") {
    git push -u origin main
    Write-Host "`n✅ Projeto enviado com sucesso!" -ForegroundColor Green
    Write-Host "🌐 Acesse: https://github.com/$username/$repoName" -ForegroundColor Cyan
} else {
    Write-Host "`n📝 Para fazer push manualmente, execute:" -ForegroundColor Yellow
    Write-Host "   git push -u origin main" -ForegroundColor White
}

Write-Host "`n✨ Pronto! Verifique o arquivo GITHUB_SETUP.md para mais informações." -ForegroundColor Green

