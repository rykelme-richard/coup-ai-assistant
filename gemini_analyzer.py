"""
Analisador avançado usando Google Gemini para análises estratégicas de Coup
"""
import google.generativeai as genai
from typing import Dict, Optional
from config import GEMINI_API_KEY, GEMINI_MODEL, USE_GEMINI
from coup_game import CoupGame, Player, Action, Character

class GeminiAnalyzer:
    """Usa Gemini para análises estratégicas avançadas"""
    
    def __init__(self):
        if USE_GEMINI and GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
                self.enabled = True
            except Exception as e:
                print(f"⚠️ Erro ao configurar Gemini: {e}")
                self.enabled = False
        else:
            self.enabled = False
    
    def analyze_situation(self, game: CoupGame, player: Player) -> Dict:
        """
        Analisa a situação do jogo usando Gemini
        Retorna análise detalhada e estratégica
        """
        if not self.enabled:
            return {"error": "Gemini não está disponível"}
        
        # Cria contexto do jogo
        context = self._create_game_context(game, player)
        
        prompt = f"""
Você é um especialista em estratégia do jogo Coup. Analise a seguinte situação e forneça recomendações estratégicas detalhadas.

{context}

Forneça:
1. Análise da situação atual (riscos e oportunidades)
2. A melhor ação recomendada e por quê
3. Análise de probabilidades das cartas dos oponentes
4. Estratégias de blefe se aplicável
5. Avisos sobre riscos específicos

Seja específico, estratégico e prático. Responda em português brasileiro.
"""
        
        try:
            response = self.model.generate_content(prompt)
            analysis = {
                "success": True,
                "analysis": response.text,
                "source": "Gemini"
            }
            return analysis
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": "Erro ao consultar Gemini"
            }
    
    def analyze_action(self, game: CoupGame, player: Player, action: Action, 
                      target: Optional[Player] = None) -> Dict:
        """
        Analisa uma ação específica usando Gemini
        """
        if not self.enabled:
            return {"error": "Gemini não está disponível"}
        
        context = self._create_game_context(game, player)
        
        action_desc = self._describe_action(action, target)
        
        prompt = f"""
Você é um especialista em estratégia do jogo Coup. Um jogador está considerando fazer a seguinte ação:

{action_desc}

Contexto do jogo:
{context}

Analise:
1. Esta é uma boa ação neste momento? Por quê?
2. Quais são os riscos?
3. Qual a probabilidade de ser desafiado?
4. Qual a probabilidade de ser bloqueado?
5. Recomendação final: fazer ou não fazer?

Responda em português brasileiro, de forma clara e estratégica.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "success": True,
                "analysis": response.text,
                "source": "Gemini"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": "Erro ao consultar Gemini"
            }
    
    def get_bluff_strategy(self, game: CoupGame, player: Player) -> Dict:
        """
        Analisa estratégia de blefe usando Gemini
        """
        if not self.enabled:
            return {"error": "Gemini não está disponível"}
        
        context = self._create_game_context(game, player)
        
        prompt = f"""
Você é um especialista em blefe no jogo Coup. Analise se o jogador deve blefar e como fazer isso estrategicamente.

{context}

Analise:
1. Deve blefar neste momento? Por quê?
2. Qual personagem seria melhor blefar?
3. Qual a probabilidade de sucesso do blefe?
4. Qual o risco se o blefe for descoberto?
5. Qual a melhor estratégia de blefe neste contexto?

Responda em português brasileiro.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "success": True,
                "analysis": response.text,
                "source": "Gemini"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": "Erro ao consultar Gemini"
            }
    
    def _create_game_context(self, game: CoupGame, player: Player) -> str:
        """Cria um contexto descritivo do jogo"""
        context = f"""
JOGADOR PRINCIPAL:
- Nome: {player.name}
- Moedas: {player.coins}
- Cartas: {', '.join([c.value for c in player.cards])}
- Cartas restantes: {len(player.cards)}

OPONENTES:
"""
        
        for opp in game.get_other_players(player):
            context += f"""
- {opp.name}:
  - Moedas: {opp.coins}
  - Cartas: {len(opp.cards)} carta(s)
  - Status: {'Eliminado' if opp.eliminated else 'Ativo'}
"""
        
        context += f"""
ESTADO DO JOGO:
- Baralho: {len(game.deck)} cartas restantes
- Jogadores ativos: {len([p for p in game.players if not p.eliminated])}
- Seu turno: {'Sim' if game.get_current_player() == player else 'Não'}
"""
        
        # Adiciona histórico recente
        if game.game_history:
            context += "\nHISTÓRICO RECENTE:\n"
            for item in game.game_history[-5:]:  # Últimas 5 ações
                context += f"- {item.get('message', 'Ação realizada')}\n"
        
        return context
    
    def _describe_action(self, action: Action, target: Optional[Player]) -> str:
        """Descreve uma ação"""
        descriptions = {
            Action.INCOME: "Income - Ganha 1 moeda (sempre permitido)",
            Action.FOREIGN_AID: "Foreign Aid - Ganha 2 moedas (pode ser bloqueado por Duque)",
            Action.TAX: "Tax (Duque) - Ganha 3 moedas",
            Action.ASSASSINATE: f"Assassinar (Assassino) - Paga 3 moedas, elimina carta de {target.name if target else 'alguém'}",
            Action.STEAL: f"Roubar (Capitão) - Rouba 2 moedas de {target.name if target else 'alguém'}",
            Action.EXCHANGE: "Trocar (Embaixador) - Troca cartas com o baralho",
            Action.COUP: f"Coup - Paga 7 moedas, elimina carta de {target.name if target else 'alguém'}"
        }
        return descriptions.get(action, action.value)
    
    def is_available(self) -> bool:
        """Verifica se o Gemini está disponível"""
        return self.enabled
