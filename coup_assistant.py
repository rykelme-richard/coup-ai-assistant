"""
Assistente de IA que ajuda o jogador humano a vencer Coup
Analisa o jogo e sugere a melhor jogada
"""
from typing import List, Dict, Optional, Tuple
from coup_game import CoupGame, Player, Action, Character
from coup_ai import CoupAI

class CoupAssistant:
    """Assistente inteligente que ajuda o jogador a vencer"""
    
    def __init__(self):
        self.ai = CoupAI(name="Assistente", difficulty="hard")
        # Tenta usar Gemini se disponível
        try:
            from gemini_analyzer import GeminiAnalyzer
            self.gemini = GeminiAnalyzer()
            self.use_gemini = self.gemini.is_available()
        except:
            self.gemini = None
            self.use_gemini = False
    
    def get_recommendation(self, game: CoupGame, player: Player) -> Dict:
        """
        Retorna recomendação completa da melhor jogada
        
        Returns:
            Dict com análise e sugestões
        """
        recommendation = {
            "best_action": None,
            "target": None,
            "should_bluff": False,
            "confidence": 0.0,
            "reasoning": "",
            "alternatives": [],
            "warnings": [],
            "tips": [],
            "gemini_analysis": None  # Análise avançada do Gemini
        }
        
        # Se Gemini está disponível, pede análise avançada
        if self.use_gemini and self.gemini:
            try:
                gemini_result = self.gemini.analyze_situation(game, player)
                if gemini_result.get("success"):
                    recommendation["gemini_analysis"] = gemini_result["analysis"]
            except:
                pass  # Continua mesmo se Gemini falhar
        
        other_players = game.get_other_players(player)
        
        if not other_players:
            recommendation["best_action"] = Action.INCOME
            recommendation["reasoning"] = "Você venceu! Não há mais oponentes."
            return recommendation
        
        # Analisa situação
        analysis = self._analyze_situation(game, player)
        
        # Recomendação 1: Coup quando possível (mais seguro)
        if player.coins >= 7:
            target = self._get_best_coup_target(game, player)
            recommendation["best_action"] = Action.COUP
            recommendation["target"] = target
            recommendation["confidence"] = 0.95
            recommendation["reasoning"] = f"Coup é a ação mais segura. Elimine {target.name} que tem {len(target.cards)} carta(s) e {target.coins} moedas."
            return recommendation
        
        # Recomendação 2: Usar poderes quando tem as cartas
        if player.has_card(Character.DUKE) and player.coins < 6:
            recommendation["best_action"] = Action.TAX
            recommendation["confidence"] = 0.9
            recommendation["reasoning"] = "Você tem Duque! Use Tax para ganhar 3 moedas sem risco de desafio."
            recommendation["tips"].append("Tax é uma das ações mais seguras quando você tem Duque.")
            return recommendation
        
        if player.has_card(Character.CAPTAIN):
            target = self._find_best_steal_target(game, player, other_players)
            if target:
                recommendation["best_action"] = Action.STEAL
                recommendation["target"] = target
                recommendation["confidence"] = 0.85
                recommendation["reasoning"] = f"Você tem Capitão! Roube de {target.name} que tem {target.coins} moedas."
                recommendation["warnings"].append(f"{target.name} pode ter Capitão ou Embaixador e bloquear.")
                return recommendation
        
        if player.has_card(Character.ASSASSIN) and player.coins >= 3:
            target = self._find_best_assassinate_target(game, player, other_players)
            if target:
                recommendation["best_action"] = Action.ASSASSINATE
                recommendation["target"] = target
                recommendation["confidence"] = 0.75
                recommendation["reasoning"] = f"Você tem Assassino! Elimine uma carta de {target.name}."
                recommendation["warnings"].append(f"{target.name} pode ter Condessa e bloquear o assassinato.")
                return recommendation
        
        # Recomendação 3: Blefe estratégico
        if player.coins >= 3:
            bluff_recommendation = self._evaluate_bluff(game, player, other_players)
            if bluff_recommendation["should_bluff"]:
                recommendation["best_action"] = bluff_recommendation["action"]
                recommendation["target"] = bluff_recommendation["target"]
                recommendation["should_bluff"] = True
                recommendation["confidence"] = 0.65
                recommendation["reasoning"] = bluff_recommendation["reasoning"]
                recommendation["warnings"].append("Você está blefando! Se desafiado, perderá uma carta.")
                return recommendation
        
        # Recomendação 4: Foreign Aid ou Income
        if len(other_players) == 1:
            # Último oponente, seja mais agressivo
            recommendation["best_action"] = Action.FOREIGN_AID
            recommendation["confidence"] = 0.7
            recommendation["reasoning"] = "Último oponente restante. Foreign Aid para ganhar moedas rapidamente."
            recommendation["warnings"].append("O oponente pode ter Duque e bloquear Foreign Aid.")
        else:
            recommendation["best_action"] = Action.FOREIGN_AID
            recommendation["confidence"] = 0.6
            recommendation["reasoning"] = "Foreign Aid é seguro e ganha 2 moedas. Melhor que Income."
            recommendation["alternatives"].append({
                "action": Action.INCOME,
                "reasoning": "Income é 100% seguro, mas ganha apenas 1 moeda."
            })
        
        return recommendation
    
    def _analyze_situation(self, game: CoupGame, player: Player) -> Dict:
        """Analisa a situação atual do jogo"""
        other_players = game.get_other_players(player)
        
        analysis = {
            "your_coins": player.coins,
            "your_cards": len(player.cards),
            "opponents_count": len(other_players),
            "richest_opponent": max(other_players, key=lambda p: p.coins) if other_players else None,
            "most_dangerous": None,
            "can_coup": player.coins >= 7,
            "can_assassinate": player.coins >= 3 and player.has_card(Character.ASSASSIN)
        }
        
        if other_players:
            # Quem é mais perigoso?
            def danger(p: Player):
                return p.coins * 2 + len(p.cards) * 3
            
            analysis["most_dangerous"] = max(other_players, key=danger)
        
        return analysis
    
    def _get_best_coup_target(self, game: CoupGame, player: Player) -> Player:
        """Encontra o melhor alvo para Coup"""
        other_players = game.get_other_players(player)
        
        # Prioriza: mais cartas > mais moedas
        def coup_priority(p: Player):
            return len(p.cards) * 10 + p.coins
        
        return max(other_players, key=coup_priority)
    
    def _find_best_steal_target(self, game: CoupGame, player: Player, 
                                targets: List[Player]) -> Optional[Player]:
        """Encontra o melhor alvo para roubar"""
        # Rouba do mais rico
        if targets:
            return max(targets, key=lambda p: p.coins)
        return None
    
    def _find_best_assassinate_target(self, game: CoupGame, player: Player,
                                     targets: List[Player]) -> Optional[Player]:
        """Encontra o melhor alvo para assassinar"""
        # Prioriza quem tem mais cartas (mais perigoso)
        if targets:
            return max(targets, key=lambda p: len(p.cards))
        return None
    
    def _evaluate_bluff(self, game: CoupGame, player: Player,
                       targets: List[Player]) -> Dict:
        """Avalia se deve blefar e qual blefe fazer"""
        recommendation = {
            "should_bluff": False,
            "action": None,
            "target": None,
            "reasoning": ""
        }
        
        # Blefa Tax (Duque) se tem poucas moedas
        if player.coins < 4:
            recommendation["should_bluff"] = True
            recommendation["action"] = Action.TAX
            recommendation["reasoning"] = "Blefe Tax para ganhar 3 moedas rapidamente. Risco médio."
            return recommendation
        
        # Blefa Steal (Capitão) se tem alvo rico
        if targets:
            rich_target = max(targets, key=lambda p: p.coins)
            if rich_target.coins >= 2:
                recommendation["should_bluff"] = True
                recommendation["action"] = Action.STEAL
                recommendation["target"] = rich_target
                recommendation["reasoning"] = f"Blefe Steal para roubar {rich_target.coins} moedas de {rich_target.name}. Risco alto."
                return recommendation
        
        return recommendation
    
    def should_challenge_action(self, game: CoupGame, player: Player,
                               target: Player, action: Action) -> Tuple[bool, str]:
        """Recomenda se deve desafiar uma ação"""
        reasoning = ""
        
        # Desafia ações perigosas
        if action == Action.ASSASSINATE:
            if len(player.cards) == 1:
                reasoning = "Você está com apenas 1 carta! Desafie para proteger."
                return True, reasoning
            else:
                reasoning = "Assassinato é perigoso. Considere desafiar."
                return True, reasoning
        
        if action == Action.STEAL:
            if player.coins >= 2:
                reasoning = "Ele está roubando suas moedas! Desafie se suspeitar."
                return True, reasoning
        
        if action == Action.TAX:
            reasoning = "Tax é uma ação comum. Só desafie se tiver certeza que ele não tem Duque."
            return False, reasoning
        
        return False, "Ação não é crítica para desafiar."
    
    def should_block_action(self, game: CoupGame, player: Player,
                          action: Action, actor: Player) -> Tuple[bool, str]:
        """Recomenda se deve bloquear uma ação"""
        reasoning = ""
        
        if action == Action.FOREIGN_AID:
            if player.has_card(Character.DUKE):
                reasoning = "Você tem Duque! Bloqueie Foreign Aid para impedir que ele ganhe 2 moedas."
                return True, reasoning
            else:
                reasoning = "Você não tem Duque. Não pode bloquear Foreign Aid."
                return False, reasoning
        
        if action == Action.STEAL:
            if player.has_card(Character.CAPTAIN) or player.has_card(Character.AMBASSADOR):
                reasoning = "Você tem carta que bloqueia roubo! Bloqueie para proteger suas moedas."
                return True, reasoning
            else:
                reasoning = "Você não pode bloquear roubo. Considere desafiar se suspeitar."
                return False, reasoning
        
        if action == Action.ASSASSINATE:
            if player.has_card(Character.CONTESSA):
                reasoning = "Você tem Condessa! Bloqueie o assassinato para proteger sua carta."
                return True, reasoning
            else:
                reasoning = "Você não tem Condessa. Não pode bloquear assassinato."
                return False, reasoning
        
        return False, "Não é possível bloquear esta ação."
