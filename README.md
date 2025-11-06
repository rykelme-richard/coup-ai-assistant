# 🎮 Sistema de IA para Vencer COUP

Sistema de inteligência artificial que joga o jogo **Coup** e ajuda você a vencer usando análise de probabilidades, blefe estratégico e modelagem de oponentes.

## 🎯 O que este sistema faz?

Este projeto cria uma **IA inteligente** que:
- ✅ **Te ajuda no jogo FÍSICO** - Use quando jogar com amigos reais!
- ✅ **Joga Coup** com estratégias avançadas (modo simulado)
- ✅ **Te ajuda a vencer** analisando o jogo e sugerindo a melhor jogada
- ✅ **Aprende padrões** dos oponentes para tomar decisões melhores
- ✅ **Calcula probabilidades** de cartas dos adversários
- ✅ **Blefa estrategicamente** quando é vantajoso

### 🎮 Modo Principal: Assistente para Jogo Físico

**A melhor funcionalidade!** Use quando você estiver jogando Coup físico com seus amigos. Você informa o estado do jogo e recebe recomendações em tempo real no seu celular/computador.

## 🚀 Funcionalidades

### 1. **Assistente de IA com Google Gemini** ✨
Um assistente que analisa o jogo em tempo real usando **Google Gemini AI** e te recomenda:
- A melhor ação para fazer
- Qual alvo escolher
- Se deve blefar ou não
- Quando desafiar/bloquear ações dos oponentes
- Análise de risco e probabilidades

### 2. **IA Avançada**
IA com 3 níveis de dificuldade:
- **Easy**: Estratégia básica
- **Medium**: Usa personagens e blefe ocasional
- **Hard**: Análise de probabilidades, blefe inteligente, modelagem de oponentes

### 3. **Simulador Completo**
Simulador completo do jogo Coup com:
- Todas as ações e regras
- Sistema de desafios e bloqueios
- Gerenciamento de cartas e moedas
- Eliminação de jogadores

## 📋 Pré-requisitos

- **Python 3.8+**
- Opcional: OpenAI API (para análises avançadas com GPT)

## 🔧 Instalação

1. **Clone ou baixe este projeto**

2. **Crie e ative o ambiente virtual:**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Mac/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure OpenAI (opcional):**
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione: `OPENAI_API_KEY=sua_chave_aqui`
   - Isso permite análises mais avançadas (mas não é obrigatório)

## 🎮 Como Usar

### 🎯 Modo 1: Assistente para JOGO FÍSICO (Recomendado!)

**Use quando você estiver jogando Coup FÍSICO com seus amigos!**

Execute o jogo:

```bash
python main.py
```

Escolha a opção **2** - Assistente para JOGO FÍSICO.

**Como funciona:**
1. Configure suas cartas e estado inicial
2. Durante o jogo, digite comandos para receber ajuda:
   - `ajuda` - Recebe recomendação da melhor jogada
   - `atualizar` - Atualiza moedas/cartas quando mudam
   - `analisar [ação] [jogador]` - Analisa uma ação específica

**Exemplo de uso durante jogo físico:**
```
💬 Comando: ajuda

💡 RECOMENDAÇÃO DO ASSISTENTE
🎯 Melhor Ação: TAX
📊 Confiança: 90%
💭 Motivo: Você tem Duque! Use Tax para ganhar 3 moedas sem risco.
```

**Quando usar:**
- Antes de fazer sua jogada → Digite `ajuda`
- Quando alguém faz uma ação → Digite `analisar roubar maria você`
- Quando o estado muda → Digite `atualizar`

### Modo 2: Jogar no Computador

Escolha a opção **1** para jogar uma partida simulada completa.

O assistente irá:
- Analisar o estado do jogo
- Recomendar a melhor jogada
- Explicar o motivo da recomendação
- Avisar sobre riscos
- Sugerir quando desafiar/bloquear

### Exemplo de Uso

```
🎮 COUP - IA ASSISTENTE 🎮

🤖 MODO: Jogador com Assistente de IA

Digite seu nome: João
Quantos oponentes IA? (1-3): 2

✅ Jogo iniciado! Você tem 2 cartas e 2 moedas.

📊 Suas informações:
   Moedas: 2
   Cartas: 2
   Suas cartas: Duque, Capitão

🤖 ASSISTENTE DE IA

💡 Recomendação: tax
   Confiança: 90%
   Motivo: Você tem Duque! Use Tax para ganhar 3 moedas sem risco de desafio.

💡 Dicas:
   - Tax é uma das ações mais seguras quando você tem Duque.

Seguir recomendação? (s/n): s
```

## 🏗️ Estrutura do Projeto

```
.
├── coup_game.py              # Simulador completo do jogo Coup
├── coup_ai.py                 # IA que joga Coup (3 níveis de dificuldade)
├── coup_assistant.py          # Assistente que ajuda o jogador humano
├── physical_game_assistant.py # 🎮 Assistente para JOGO FÍSICO (principal!)
├── main.py                    # Interface principal do jogo
├── config.py                  # Configurações (opcional)
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🧠 Como a IA Funciona

### Estratégias da IA

1. **Análise de Probabilidades**
   - Calcula a probabilidade de cada oponente ter cada carta
   - Baseado em cartas já reveladas e ações anteriores

2. **Blefe Inteligente**
   - Decide quando blefar baseado em risco vs. recompensa
   - Avalia probabilidade de ser desafiado

3. **Modelagem de Oponentes**
   - Observa padrões de comportamento
   - Ajusta estratégia baseado em histórico

4. **Priorização de Ações**
   - **Coup** quando possível (mais seguro)
   - **Tax** quando tem Duque (ganho seguro)
   - **Steal** quando tem Capitão (rouba moedas)
   - **Assassinate** quando tem Assassino e alvo vulnerável

### Recomendações do Assistente

O assistente analisa:
- **Sua situação**: moedas, cartas, oponentes
- **Melhor ação**: qual ação te dá mais vantagem
- **Melhor alvo**: quem atacar prioriza
- **Riscos**: probabilidade de desafio/bloqueio
- **Alternativas**: outras opções viáveis

## 🎯 Personagens do Jogo

- **Duque**: Tax (ganha 3 moedas) | Bloqueia Foreign Aid
- **Assassino**: Assassinar (paga 3, elimina carta)
- **Capitão**: Roubar (rouba 2 moedas) | Bloqueia roubo
- **Embaixador**: Trocar cartas | Bloqueia roubo
- **Condessa**: Bloqueia assassinato

## 📊 Exemplo de Análise do Assistente

```
🤖 ASSISTENTE DE IA

💡 Recomendação: coup
   Alvo: IA1
   Confiança: 95%
   Motivo: Coup é a ação mais segura. Elimine IA1 que tem 2 carta(s) e 5 moedas.

⚠️ Avisos:
   - Nenhum aviso para esta ação.

💡 Dicas:
   - Coup não pode ser bloqueado ou desafiado.
   - Use quando tiver 7+ moedas para eliminar ameaças.
```

## 🔄 Fluxo do Jogo

1. **Início**: Cada jogador recebe 2 cartas e 2 moedas
2. **Turnos**: Jogadores alternam fazendo ações
3. **Ações**: Income, Foreign Aid, ou usar poderes dos personagens
4. **Desafios**: Outros podem desafiar se não acreditarem
5. **Bloqueios**: Algumas ações podem ser bloqueadas
6. **Eliminação**: Perde 2 cartas = eliminado
7. **Vitória**: Último jogador com carta vence

## 🎓 Estratégias Aprendidas

A IA usa técnicas de:
- **Teoria de Jogos**: Análise de estratégias dominantes
- **Probabilidade Bayesiana**: Atualização de crenças sobre cartas
- **Aprendizado por Reforço**: Ajuste de estratégias baseado em resultados
- **Modelagem de Adversários**: Previsão de ações dos oponentes

## 🐛 Solução de Problemas

**Erro ao executar:**
- Certifique-se de que o venv está ativado
- Instale as dependências: `pip install -r requirements.txt`

**IA não está ajudando:**
- A IA funciona melhor com mais informações (histórico de ações)
- Quanto mais você joga, melhor ela fica em analisar padrões

## 🚀 Próximas Melhorias

- [ ] Interface gráfica (GUI)
- [ ] Análise com GPT-4 para explicações mais detalhadas
- [ ] Modo de treinamento (IA vs IA)
- [ ] Estatísticas de vitória
- [ ] Salvamento de partidas
- [ ] Análise pós-jogo

## 📝 Licença

Este projeto é para uso educacional e pessoal.

## 🤝 Contribuindo

Sinta-se livre para melhorar:
- Adicionar novas estratégias
- Melhorar análise de probabilidades
- Criar interface gráfica
- Otimizar algoritmos

---

**Desenvolvido para criar uma IA que vence Coup! 🎮🤖**
