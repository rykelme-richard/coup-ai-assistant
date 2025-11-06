"""
IA Inteligente para jogar Coup
Utiliza análise de probabilidades, blefe estratégico e modelagem de oponentes
"""
import random
from typing import List, Dict, Optional, Tuple
from coup_game import CoupGame, Player, Action, Character

class CoupAI:
    """IA que joga Coup usando estratégias avançadas"""
    
    def __init__(self, name: str = "IA", difficulty: str = "hard", learning_params: Dict = None):
        """
        Args:
            name: Nome da IA
            difficulty: "easy", "medium", "hard"
            learning_params: Parâmetros aprendidos (opcional)
        """
        self.name = name
        self.difficulty = difficulty
        self.memory = {}  # Memória de ações dos oponentes
        self.opponent_models = {}  # Modelos de comportamento dos oponentes
        
        # Parâmetros de aprendizado
        if learning_params:
            self.learning_params = learning_params
        else:
            self.learning_params = {
                "bluff_probability": 0.4,
                "challenge_aggressiveness": 0.5,
                "block_probability": 0.7,
                "tax_preference": 0.8,
                "steal_preference": 0.6,
                "assassinate_preference": 0.5
            }
    
    def choose_action(self, game: CoupGame, player: Player) -> Tuple[Action, Optional[Player], bool]:
        """
        Escolhe a melhor ação para o jogador
        
        Returns:
            (action, target, is_bluff)
        """
        if self.difficulty == "easy":
            return self._easy_strategy(game, player)
        elif self.difficulty == "medium":
            return self._medium_strategy(game, player)
        else:
            return self._hard_strategy(game, player)
    
    def _easy_strategy(self, game: CoupGame, player: Player) -> Tuple[Action, Optional[Player], bool]:
        """Estratégia simples: sempre Income ou Foreign Aid"""
        if player.coins >= 7:
            # Pode fazer Coup
            targets = game.get_other_players(player)
            if targets:
                return (Action.COUP, random.choice(targets), False)
        
        # Tenta Foreign Aid
        if random.random() < 0.7:
            return (Action.FOREIGN_AID, None, False)
        else:
            return (Action.INCOME, None, False)
    
    def _medium_strategy(self, game: CoupGame, player: Player) -> Tuple[Action, Optional[Player], bool]:
        """Estratégia média: usa personagens quando tem, blefe ocasional"""
        other_players = game.get_other_players(player)
        
        if not other_players:
            return (Action.INCOME, None, False)
        
        # Se tem 7+ moedas, faz Coup
        if player.coins >= 7:
            # Escolhe o jogador com mais cartas (maior ameaça)
            target = max(other_players, key=lambda p: len(p.cards))
            return (Action.COUP, target, False)
        
        # Usa poderes se tem as cartas
        if player.has_card(Character.DUKE) and player.coins < 6:
            return (Action.TAX, None, False)
        
        if player.has_card(Character.CAPTAIN):
            # Rouba do jogador mais rico
            rich_target = max(other_players, key=lambda p: p.coins)
            if rich_target.coins >= 1:
                return (Action.STEAL, rich_target, False)
        
        if player.has_card(Character.ASSASSIN) and player.coins >= 3:
            # Assassina se tiver moedas
            target = random.choice(other_players)
            return (Action.ASSASSINATE, target, False)
        
        # Blefe ocasional (30% chance)
        if random.random() < 0.3:
            if random.random() < 0.5:
                return (Action.TAX, None, True)  # Blefa Duque
            else:
                rich_target = max(other_players, key=lambda p: p.coins)
                if rich_target.coins >= 1:
                    return (Action.STEAL, rich_target, True)  # Blefa Capitão
        
        # Default: Foreign Aid ou Income
        if random.random() < 0.6:
            return (Action.FOREIGN_AID, None, False)
        else:
            return (Action.INCOME, None, False)
    
    def _hard_strategy(self, game: CoupGame, player: Player) -> Tuple[Action, Optional[Player], bool]:
        """Estratégia avançada: análise de probabilidades, blefe inteligente, modelagem de oponentes"""
        other_players = game.get_other_players(player)
        
        if not other_players:
            return (Action.INCOME, None, False)
        
        # Calcula probabilidades de cartas dos oponentes
        probabilities = self._calculate_probabilities(game, player)
        
        # Estratégia 1: Coup quando possível (mais seguro)
        if player.coins >= 7:
            # Elimina o jogador mais perigoso
            target = self._get_most_dangerous_player(game, player, probabilities)
            return (Action.COUP, target, False)
        
        # Estratégia 2: Usa poderes quando tem
        if player.has_card(Character.DUKE):
            if player.coins < 6:
                return (Action.TAX, None, False)
        
        if player.has_card(Character.CAPTAIN):
            # Rouba do jogador mais rico que provavelmente não tem Capitão
            safe_target = self._find_safe_steal_target(other_players, probabilities)
            if safe_target:
                return (Action.STEAL, safe_target, False)
        
        if player.has_card(Character.ASSASSIN) and player.coins >= 3:
            # Assassina se o alvo provavelmente não tem Condessa
            target = self._find_vulnerable_target(other_players, probabilities)
            if target:
                return (Action.ASSASSINATE, target, False)
        
        # Estratégia 3: Blefe inteligente (usa parâmetros aprendidos)
        bluff_prob = self.learning_params.get("bluff_probability", 0.4)
        if player.coins >= 3 and random.random() < bluff_prob:
            # Blefa se a probabilidade de ser desafiado é baixa
            bluff_action, target = self._smart_bluff(other_players, probabilities)
            if bluff_action:
                return (bluff_action, target, True)
        
        # Estratégia 4: Foreign Aid (seguro, mas pode ser bloqueado)
        if random.random() < 0.7:
            return (Action.FOREIGN_AID, None, False)
        else:
            return (Action.INCOME, None, False)
    
    def _calculate_probabilities(self, game: CoupGame, player: Player) -> Dict[str, Dict[Character, float]]:
        """Calcula probabilidades de cada oponente ter cada carta"""
        probabilities = {}
        
        # Cartas conhecidas (já reveladas)
        known_cards = []
        for history_item in game.game_history:
            # Pode inferir cartas de ações anteriores
            pass  # TODO: Implementar inferência de cartas do histórico
        
        # Para cada oponente
        for opponent in game.get_other_players(player):
            probs = {}
            total_possible = len(game.deck) + sum(len(p.cards) for p in game.players if p != player)
            
            # Distribuição inicial: cada carta tem 3 cópias no baralho
            for char in Character:
                # Simplificado: assume distribuição uniforme
                probs[char] = 0.3  # ~30% chance (3 de 10 cartas possíveis)
            
            probabilities[opponent.name] = probs
        
        return probabilities
    
    def _get_most_dangerous_player(self, game: CoupGame, player: Player, 
                                  probabilities: Dict) -> Player:
        """Identifica o jogador mais perigoso"""
        other_players = game.get_other_players(player)
        
        # Cálculo de perigo: moedas + cartas + probabilidade de ter Assassino
        def danger_score(p: Player) -> float:
            score = p.coins * 2  # Moedas = poder
            score += len(p.cards) * 3  # Mais cartas = mais perigoso
            
            # Se provavelmente tem Assassino, é mais perigoso
            if p.name in probabilities:
                score += probabilities[p.name].get(Character.ASSASSIN, 0) * 5
            
            return score
        
        return max(other_players, key=danger_score)
    
    def _find_safe_steal_target(self, targets: List[Player], 
                                probabilities: Dict) -> Optional[Player]:
        """Encontra alvo seguro para roubar (baixa probabilidade de ter Capitão)"""
        safe_targets = []
        
        for target in targets:
            if target.coins < 1:
                continue
            
            # Se tem pouca chance de ter Capitão, é seguro
            if target.name in probabilities:
                captain_prob = probabilities[target.name].get(Character.CAPTAIN, 0.3)
                if captain_prob < 0.4:
                    safe_targets.append((target, target.coins, captain_prob))
        
        if safe_targets:
            # Prioriza quem tem mais moedas e menor chance de bloquear
            safe_targets.sort(key=lambda x: (x[1], -x[2]))
            return safe_targets[0][0]
        
        # Se não achou seguro, rouba do mais rico
        if targets:
            return max(targets, key=lambda p: p.coins)
        
        return None
    
    def _find_vulnerable_target(self, targets: List[Player], 
                               probabilities: Dict) -> Optional[Player]:
        """Encontra alvo vulnerável para assassinato (baixa probabilidade de ter Condessa)"""
        vulnerable_targets = []
        
        for target in targets:
            if target.name in probabilities:
                contessa_prob = probabilities[target.name].get(Character.CONTESSA, 0.3)
                # Se tem baixa chance de ter Condessa, é vulnerável
                if contessa_prob < 0.4:
                    vulnerable_targets.append((target, contessa_prob))
        
        if vulnerable_targets:
            # Escolhe o mais vulnerável
            vulnerable_targets.sort(key=lambda x: x[1])
            return vulnerable_targets[0][0]
        
        return random.choice(targets) if targets else None
    
    def _smart_bluff(self, targets: List[Player], 
                    probabilities: Dict) -> Tuple[Optional[Action], Optional[Player]]:
        """Decide qual blefe fazer e em quem"""
        # Blefa Duque (Tax) se tem poucas moedas
        # Blefa Capitão (Steal) se tem alvo rico
        
        if targets:
            rich_target = max(targets, key=lambda p: p.coins)
            if rich_target.coins >= 2:
                # Blefa Capitão para roubar
                return (Action.STEAL, rich_target)
        
        # Blefa Duque para ganhar moedas
        return (Action.TAX, None)
    
    def should_challenge(self, game: CoupGame, challenger: Player, 
                        target: Player, action: Action) -> bool:
        """Decide se deve desafiar uma ação (usa parâmetros aprendidos)"""
        if self.difficulty == "easy":
            return random.random() < 0.2  # 20% chance
        
        if self.difficulty == "medium":
            # Desafia se tem pouca confiança
            return random.random() < 0.4
        
        # Hard: análise mais sofisticada com parâmetros aprendidos
        challenge_agg = self.learning_params.get("challenge_aggressiveness", 0.5)
        
        # Se a ação é muito perigosa, desafia mais
        if action in [Action.ASSASSINATE, Action.STEAL]:
            if challenger.coins < 2:  # Desafia para proteger moedas
                return random.random() < (0.4 + challenge_agg * 0.4)
        
        # Se tem poucas cartas, menos provável que desafie
        if len(challenger.cards) == 1:
            return random.random() < (0.2 + challenge_agg * 0.2)
        
        return random.random() < challenge_agg
    
    def should_block(self, game: CoupGame, blocker: Player, 
                    action: Action, actor: Player) -> bool:
        """Decide se deve bloquear uma ação"""
        if blocker.eliminated:
            return False
        
        # Se tem a carta, sempre bloqueia ações perigosas
        if action == Action.FOREIGN_AID and blocker.has_card(Character.DUKE):
            return True
        
        if action == Action.STEAL:
            if blocker.has_card(Character.CAPTAIN) or blocker.has_card(Character.AMBASSADOR):
                return True
        
        if action == Action.ASSASSINATE and blocker.has_card(Character.CONTESSA):
            return True
        
        # Blefe de bloqueio (risco)
        if self.difficulty == "hard" and random.random() < 0.3:
            if action == Action.STEAL and blocker.coins >= 2:
                return True  # Blefa bloqueio
        
        return False
    
    def update_memory(self, player_name: str, action: Action, was_bluff: bool):
        """Atualiza memória sobre ações dos jogadores"""
        if player_name not in self.memory:
            self.memory[player_name] = []
        
        self.memory[player_name].append({
            "action": action,
            "was_bluff": was_bluff
        })
