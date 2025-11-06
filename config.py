"""
Configurações para o sistema de IA do Coup
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da API OpenAI (opcional, para análises avançadas)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Configurações da API Google Gemini (opcional, para análises avançadas)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
USE_GEMINI = os.getenv("USE_GEMINI", "true").lower() == "true"

# Configurações do jogo
DEFAULT_AI_DIFFICULTY = "hard"  # "easy", "medium", "hard"
MAX_PLAYERS = 6
MIN_PLAYERS = 2

# Informações sobre o jogo Coup
COUP_CHARACTERS = {
    "Duque": {
        "action": "Tax",
        "description": "Ganha 3 moedas",
        "block": "Bloqueia Foreign Aid"
    },
    "Assassino": {
        "action": "Assassinar",
        "description": "Paga 3 moedas, elimina uma carta do alvo",
        "block": None
    },
    "Capitão": {
        "action": "Roubar",
        "description": "Rouba 2 moedas de outro jogador",
        "block": "Bloqueia roubo (Capitão ou Embaixador)"
    },
    "Embaixador": {
        "action": "Trocar",
        "description": "Troca cartas com o baralho",
        "block": "Bloqueia roubo"
    },
    "Condessa": {
        "action": None,
        "description": "Não tem ação própria",
        "block": "Bloqueia assassinato"
    }
}

COUP_RULES = """
COUP - Regras Básicas:
- Cada jogador começa com 2 cartas de personagem e 2 moedas
- Você pode realizar ações baseadas nos personagens que tem (ou fingir que tem)
- Outros jogadores podem desafiar você se não acreditar que você tem aquele personagem
- Se você perde uma carta, você perde uma "vida"
- Se você perder ambas as cartas, está eliminado
- O último jogador com pelo menos uma carta vence

Ações Básicas:
- Income: Ganha 1 moeda (sempre permitido)
- Foreign Aid: Ganha 2 moedas (pode ser bloqueado por Duque)
- Coup: Paga 7 moedas, elimina carta de alguém (não pode ser bloqueado)

Desafios:
- Qualquer um pode desafiar uma ação
- Se estava blefando: perde uma carta
- Se tinha a carta: quem desafiou perde uma carta
"""