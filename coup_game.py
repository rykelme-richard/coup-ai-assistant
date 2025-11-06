"""
Simulador completo do jogo Coup
"""
import random
from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

class Character(Enum):
    """Personagens do jogo Coup"""
    DUKE = "Duque"
    ASSASSIN = "Assassino"
    CAPTAIN = "Capitão"
    AMBASSADOR = "Embaixador"
    CONTESSA = "Condessa"

class Action(Enum):
    """Ações disponíveis no jogo"""
    INCOME = "income"  # Ganha 1 moeda
    FOREIGN_AID = "foreign_aid"  # Ganha 2 moedas (pode ser bloqueado)
    COUP = "coup"  # Paga 7 moedas, elimina carta de alguém
    TAX = "tax"  # Duque: ganha 3 moedas
    ASSASSINATE = "assassinate"  # Assassino: paga 3, elimina carta
    STEAL = "steal"  # Capitão: rouba 2 moedas
    EXCHANGE = "exchange"  # Embaixador: troca cartas
    BLOCK_FOREIGN_AID = "block_foreign_aid"  # Duque bloqueia foreign aid
    BLOCK_STEAL = "block_steal"  # Capitão/Embaixador bloqueia roubo
    BLOCK_ASSASSINATE = "block_assassinate"  # Condessa bloqueia assassinato

@dataclass
class Player:
    """Representa um jogador no jogo"""
    name: str
    coins: int = 2
    cards: List[Character] = None
    eliminated: bool = False
    
    def __post_init__(self):
        if self.cards is None:
            self.cards = []
    
    def lose_card(self, card: Character) -> bool:
        """Remove uma carta do jogador. Retorna True se foi eliminado."""
        if card in self.cards:
            self.cards.remove(card)
            if len(self.cards) == 0:
                self.eliminated = True
            return self.eliminated
        return False
    
    def has_card(self, card: Character) -> bool:
        """Verifica se o jogador tem uma carta"""
        return card in self.cards

class CoupGame:
    """Classe principal do jogo Coup"""
    
    # Deck completo: 3 cópias de cada personagem
    FULL_DECK = [char for char in Character for _ in range(3)]
    
    def __init__(self, player_names: List[str]):
        """
        Inicializa o jogo
        
        Args:
            player_names: Lista com nomes dos jogadores
        """
        if len(player_names) < 2:
            raise ValueError("Precisa de pelo menos 2 jogadores")
        
        self.players = [Player(name) for name in player_names]
        self.deck = self.FULL_DECK.copy()
        self.current_player_index = 0
        self.game_history = []
        
        # Distribui cartas
        self._deal_cards()
    
    def _deal_cards(self):
        """Distribui 2 cartas para cada jogador"""
        random.shuffle(self.deck)
        
        for player in self.players:
            if len(self.deck) >= 2:
                player.cards = [self.deck.pop(), self.deck.pop()]
            else:
                raise ValueError("Não há cartas suficientes no baralho")
    
    def get_current_player(self) -> Player:
        """Retorna o jogador atual"""
        return self.players[self.current_player_index]
    
    def get_other_players(self, exclude_player: Player) -> List[Player]:
        """Retorna todos os outros jogadores"""
        return [p for p in self.players if p != exclude_player and not p.eliminated]
    
    def get_game_state(self, player: Optional[Player] = None) -> Dict:
        """
        Retorna o estado atual do jogo
        
        Args:
            player: Se fornecido, retorna informações específicas para esse jogador
        """
        state = {
            "current_player": self.current_player_index,
            "players": []
        }
        
        for p in self.players:
            player_info = {
                "name": p.name,
                "coins": p.coins,
                "cards_count": len(p.cards),
                "eliminated": p.eliminated
            }
            
            # Se for o jogador solicitado, mostra suas cartas
            if player and p == player:
                player_info["cards"] = [card.value for card in p.cards]
            else:
                # Para outros jogadores, apenas quantidade de cartas
                player_info["cards"] = None
            
            state["players"].append(player_info)
        
        state["deck_size"] = len(self.deck)
        state["history"] = self.game_history[-10:]  # Últimas 10 ações
        
        return state
    
    def is_valid_action(self, action: Action, player: Player, target: Optional[Player] = None) -> Tuple[bool, str]:
        """
        Verifica se uma ação é válida
        
        Returns:
            (is_valid, error_message)
        """
        if player.eliminated:
            return False, "Jogador eliminado"
        
        if action == Action.INCOME:
            return True, ""
        
        if action == Action.FOREIGN_AID:
            return True, ""
        
        if action == Action.COUP:
            if player.coins < 7:
                return False, "Precisa de 7 moedas para fazer Coup"
            if not target:
                return False, "Coup precisa de um alvo"
            if target.eliminated:
                return False, "Alvo está eliminado"
            return True, ""
        
        if action == Action.TAX:
            if not player.has_card(Character.DUKE):
                return False, "Precisa ter Duque para fazer Tax"
            return True, ""
        
        if action == Action.ASSASSINATE:
            if player.coins < 3:
                return False, "Precisa de 3 moedas para Assassinar"
            if not player.has_card(Character.ASSASSIN):
                return False, "Precisa ter Assassino para Assassinar"
            if not target:
                return False, "Assassinar precisa de um alvo"
            if target.eliminated:
                return False, "Alvo está eliminado"
            return True, ""
        
        if action == Action.STEAL:
            if not player.has_card(Character.CAPTAIN):
                return False, "Precisa ter Capitão para Roubar"
            if not target:
                return False, "Roubar precisa de um alvo"
            if target.coins < 1:
                return False, "Alvo não tem moedas para roubar"
            if target.eliminated:
                return False, "Alvo está eliminado"
            return True, ""
        
        if action == Action.EXCHANGE:
            if not player.has_card(Character.AMBASSADOR):
                return False, "Precisa ter Embaixador para Trocar"
            return True, ""
        
        return False, "Ação não reconhecida"
    
    def execute_action(self, action: Action, player: Player, target: Optional[Player] = None, 
                      bluff: bool = False, challenged: bool = False) -> Dict:
        """
        Executa uma ação no jogo
        
        Args:
            action: Ação a executar
            player: Jogador que executa
            target: Alvo da ação (se aplicável)
            bluff: Se o jogador está blefando (não tem a carta)
            challenged: Se alguém desafiou a ação
        
        Returns:
            Dict com resultado da ação
        """
        result = {
            "success": False,
            "message": "",
            "action": action.value,
            "player": player.name,
            "target": target.name if target else None
        }
        
        # Verifica se é válida
        is_valid, error = self.is_valid_action(action, player, target)
        if not is_valid and not bluff:
            result["message"] = error
            return result
        
        # Executa ação
        if action == Action.INCOME:
            player.coins += 1
            result["success"] = True
            result["message"] = f"{player.name} ganhou 1 moeda"
        
        elif action == Action.FOREIGN_AID:
            player.coins += 2
            result["success"] = True
            result["message"] = f"{player.name} ganhou 2 moedas (Foreign Aid)"
        
        elif action == Action.COUP:
            player.coins -= 7
            if target:
                # Remove uma carta aleatória do alvo
                if target.cards:
                    card = random.choice(target.cards)
                    eliminated = target.lose_card(card)
                    result["success"] = True
                    result["message"] = f"{player.name} fez Coup em {target.name}, eliminou {card.value}"
                    if eliminated:
                        result["message"] += f" - {target.name} foi eliminado!"
        
        elif action == Action.TAX:
            player.coins += 3
            result["success"] = True
            result["message"] = f"{player.name} usou Tax (Duque), ganhou 3 moedas"
        
        elif action == Action.ASSASSINATE:
            player.coins -= 3
            if target and target.cards:
                card = random.choice(target.cards)
                eliminated = target.lose_card(card)
                result["success"] = True
                result["message"] = f"{player.name} assassinou {target.name}, eliminou {card.value}"
                if eliminated:
                    result["message"] += f" - {target.name} foi eliminado!"
        
        elif action == Action.STEAL:
            stolen = min(2, target.coins)
            player.coins += stolen
            target.coins -= stolen
            result["success"] = True
            result["message"] = f"{player.name} roubou {stolen} moedas de {target.name}"
        
        elif action == Action.EXCHANGE:
            # Troca cartas com o baralho
            if len(self.deck) >= 2:
                # Retorna cartas ao baralho
                returned = player.cards[:]
                for card in returned:
                    if card in player.cards:
                        player.cards.remove(card)
                        self.deck.append(card)
                
                # Pega novas cartas
                random.shuffle(self.deck)
                new_cards = [self.deck.pop(), self.deck.pop()]
                player.cards = new_cards
                result["success"] = True
                result["message"] = f"{player.name} trocou cartas com o baralho"
        
        # Registra no histórico
        self.game_history.append(result)
        
        return result
    
    def next_turn(self):
        """Avança para o próximo turno"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Pula jogadores eliminados
        while self.players[self.current_player_index].eliminated:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def get_winner(self) -> Optional[Player]:
        """Retorna o vencedor do jogo (se houver)"""
        active_players = [p for p in self.players if not p.eliminated]
        if len(active_players) == 1:
            return active_players[0]
        return None
    
    def is_game_over(self) -> bool:
        """Verifica se o jogo terminou"""
        return self.get_winner() is not None
