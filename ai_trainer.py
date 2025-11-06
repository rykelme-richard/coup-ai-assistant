"""
Sistema de Treinamento para IA de Coup
Permite que IAs joguem entre si e aprendam com as experiências
"""
import random
from typing import List, Dict, Tuple, Optional
from coup_game import CoupGame, Player, Action, Character
from coup_ai import CoupAI
from ai_learning import AILearning

class AITrainer:
    """Sistema de treinamento para IAs"""
    
    def __init__(self):
        self.training_stats = {
            "games_played": 0,
            "wins_by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
            "learning_data": []
        }
        # Sistema de aprendizado persistente
        self.learning = AILearning()
    
    def train_ai(self, num_games: int = 100, ai_difficulty: str = "hard", 
                 opponent_difficulties: List[str] = ["easy", "medium"]):
        """
        Treina uma IA fazendo ela jogar múltiplas partidas COM APRENDIZADO PERSISTENTE
        
        Args:
            num_games: Número de partidas para treinar
            ai_difficulty: Dificuldade da IA sendo treinada
            opponent_difficulties: Lista de dificuldades dos oponentes
        """
        print(f"\n{'='*60}")
        print(f"🎓 TREINANDO IA ({ai_difficulty.upper()}) COM APRENDIZADO")
        print(f"{'='*60}")
        print(f"Partidas: {num_games}")
        print(f"Oponentes: {opponent_difficulties}")
        
        # Mostra conhecimento prévio
        if self.learning.learning_data["total_games"] > 0:
            prev_win_rate = self.learning.get_win_rate() * 100
            print(f"Conhecimento prévio: {self.learning.learning_data['total_games']} partidas, {prev_win_rate:.1f}% vitórias")
            print(f"Parâmetros atuais: Blefe={self.learning.learning_data['strategy_params']['bluff_probability']:.2f}, "
                  f"Desafio={self.learning.learning_data['strategy_params']['challenge_aggressiveness']:.2f}")
        print(f"{'='*60}\n")
        
        wins = 0
        losses = 0
        
        for game_num in range(1, num_games + 1):
            # Carrega parâmetros aprendidos
            learned_params = self.learning.get_strategy_params()
            
            # Cria IA com parâmetros aprendidos
            trained_ai = CoupAI(name="IA_Treinada", difficulty=ai_difficulty, learning_params=learned_params)
            opponents = []
            
            # Cria oponentes com diferentes dificuldades
            for i, diff in enumerate(opponent_difficulties):
                opponents.append(CoupAI(name=f"Oponente_{i+1}", difficulty=diff))
            
            # Cria jogo
            all_names = [trained_ai.name] + [opp.name for opp in opponents]
            game = CoupGame(all_names)
            
            # Joga até o fim
            winner = self._play_game(game, trained_ai, opponents)
            
            # Registra resultado e aprende
            won = winner and winner.name == trained_ai.name
            if won:
                wins += 1
                self.training_stats["wins_by_difficulty"][ai_difficulty] += 1
            else:
                losses += 1
            
            # Aprende com o resultado
            self.learning.record_game_result(won)
            recent_win_rate = self.learning.get_recent_win_rate(10)
            self.learning.learn_from_results(won, recent_win_rate)
            
            # Salva aprendizado a cada 10 partidas
            if game_num % 10 == 0:
                win_rate = (wins / game_num) * 100
                print(f"Partida {game_num}/{num_games} | Vitórias: {wins} ({win_rate:.1f}%)")
                print(f"   Parâmetros aprendidos: Blefe={self.learning.learning_data['strategy_params']['bluff_probability']:.2f}, "
                      f"Desafio={self.learning.learning_data['strategy_params']['challenge_aggressiveness']:.2f}")
                self.learning.save_learning()  # Salva progresso
            
            self.training_stats["games_played"] += 1
        
        # Salva aprendizado final
        self.learning.save_learning()
        
        # Resultados finais
        final_win_rate = (wins / num_games) * 100
        print(f"\n{'='*60}")
        print(f"✅ TREINAMENTO CONCLUÍDO")
        print(f"{'='*60}")
        print(f"Vitórias: {wins}/{num_games} ({final_win_rate:.1f}%)")
        print(f"Derrotas: {losses}/{num_games}")
        print(f"\n💾 Conhecimento salvo em: {self.learning.LEARNING_FILE}")
        print(f"   Total de partidas (todas sessões): {self.learning.learning_data['total_games']}")
        print(f"   Taxa de vitória geral: {self.learning.get_win_rate()*100:.1f}%")
        print(f"{'='*60}\n")
        
        return {
            "wins": wins,
            "losses": losses,
            "win_rate": final_win_rate
        }
    
    def _play_game(self, game: CoupGame, trained_ai: CoupAI, 
                   opponents: List[CoupAI]) -> Player:
        """Joga uma partida completa"""
        max_turns = 200  # Limite de segurança
        
        for turn in range(max_turns):
            if game.is_game_over():
                break
            
            current_player = game.get_current_player()
            
            # Encontra a IA correspondente
            ai = None
            if current_player.name == trained_ai.name:
                ai = trained_ai
            else:
                ai = next((o for o in opponents if o.name == current_player.name), None)
            
            if not ai:
                # Se não encontrou IA, pula turno
                game.next_turn()
                continue
            
            # IA escolhe ação
            action, target, is_bluff = ai.choose_action(game, current_player)
            
            # Executa ação
            result = game.execute_action(action, current_player, target, is_bluff)
            
            # Outros jogadores podem desafiar/bloquear
            self._handle_reactions(game, current_player, action, target, 
                                 trained_ai, opponents, is_bluff)
            
            # Próximo turno
            game.next_turn()
            
            # Verifica vencedor
            winner = game.get_winner()
            if winner:
                return winner
        
        # Retorna vencedor ou None
        return game.get_winner()
    
    def _handle_reactions(self, game: CoupGame, actor: Player, action: Action,
                         target: Optional[Player], trained_ai: CoupAI,
                         opponents: List[CoupAI], was_bluff: bool):
        """Lida com reações (bloqueios e desafios)"""
        other_players = game.get_other_players(actor)
        
        for player in other_players:
            if player.eliminated:
                continue
            
            # Encontra IA correspondente
            ai = None
            if player.name == trained_ai.name:
                ai = trained_ai
            else:
                ai = next((o for o in opponents if o.name == player.name), None)
            
            if not ai:
                continue
            
            # Bloqueios
            if action == Action.FOREIGN_AID:
                if ai.should_block(game, player, action, actor):
                    if player.has_card(Character.DUKE) or random.random() < 0.5:
                        # Bloqueia (pode ser blefe)
                        actor.coins -= 2
                        return
            
            elif action == Action.STEAL and target == player:
                if ai.should_block(game, player, action, actor):
                    if (player.has_card(Character.CAPTAIN) or 
                        player.has_card(Character.AMBASSADOR) or 
                        random.random() < 0.4):
                        # Bloqueia roubo
                        return
            
            elif action == Action.ASSASSINATE and target == player:
                if ai.should_block(game, player, action, actor):
                    if player.has_card(Character.CONTESSA) or random.random() < 0.3:
                        # Bloqueia assassinato
                        return
            
            # Desafios
            if action in [Action.TAX, Action.ASSASSINATE, Action.STEAL, Action.EXCHANGE]:
                if ai.should_challenge(game, player, actor, action):
                    # Processa desafio
                    if was_bluff:
                        # Blefe descoberto!
                        if actor.cards:
                            card = actor.cards[0]
                            actor.lose_card(card)
                    else:
                        # Desafio falhou!
                        if player.cards:
                            card = player.cards[0]
                            player.lose_card(card)
                    return
    
    def compare_ai_levels(self, num_games: int = 50):
        """Compara diferentes níveis de IA jogando entre si"""
        print(f"\n{'='*60}")
        print(f"⚔️ COMPARAÇÃO DE NÍVEIS DE IA")
        print(f"{'='*60}")
        print(f"Partidas por comparação: {num_games}")
        print(f"{'='*60}\n")
        
        # Resultados por comparação
        comparison_results = {}
        
        # Easy vs Medium
        print("🔄 Easy vs Medium...")
        easy_wins = 0
        medium_wins = 0
        for _ in range(num_games):
            winner = self._play_1v1("easy", "medium")
            if winner == "easy":
                easy_wins += 1
            elif winner == "medium":
                medium_wins += 1
        
        comparison_results["Easy vs Medium"] = {
            "easy": easy_wins,
            "medium": medium_wins,
            "total": num_games
        }
        print(f"   ✅ Easy: {easy_wins}/{num_games} ({easy_wins/num_games*100:.1f}%)")
        print(f"   ✅ Medium: {medium_wins}/{num_games} ({medium_wins/num_games*100:.1f}%)")
        
        # Medium vs Hard
        print("\n🔄 Medium vs Hard...")
        medium_wins = 0
        hard_wins = 0
        for _ in range(num_games):
            winner = self._play_1v1("medium", "hard")
            if winner == "medium":
                medium_wins += 1
            elif winner == "hard":
                hard_wins += 1
        
        comparison_results["Medium vs Hard"] = {
            "medium": medium_wins,
            "hard": hard_wins,
            "total": num_games
        }
        print(f"   ✅ Medium: {medium_wins}/{num_games} ({medium_wins/num_games*100:.1f}%)")
        print(f"   ✅ Hard: {hard_wins}/{num_games} ({hard_wins/num_games*100:.1f}%)")
        
        # Easy vs Hard
        print("\n🔄 Easy vs Hard...")
        easy_wins = 0
        hard_wins = 0
        for _ in range(num_games):
            winner = self._play_1v1("easy", "hard")
            if winner == "easy":
                easy_wins += 1
            elif winner == "hard":
                hard_wins += 1
        
        comparison_results["Easy vs Hard"] = {
            "easy": easy_wins,
            "hard": hard_wins,
            "total": num_games
        }
        print(f"   ✅ Easy: {easy_wins}/{num_games} ({easy_wins/num_games*100:.1f}%)")
        print(f"   ✅ Hard: {hard_wins}/{num_games} ({hard_wins/num_games*100:.1f}%)")
        
        # Resumo geral
        print(f"\n{'='*60}")
        print(f"📊 RESUMO GERAL")
        print(f"{'='*60}")
        
        # Calcula totais
        total_easy_wins = (comparison_results["Easy vs Medium"]["easy"] + 
                          comparison_results["Easy vs Hard"]["easy"])
        total_easy_games = comparison_results["Easy vs Medium"]["total"] + comparison_results["Easy vs Hard"]["total"]
        
        total_medium_wins = (comparison_results["Easy vs Medium"]["medium"] + 
                            comparison_results["Medium vs Hard"]["medium"])
        total_medium_games = comparison_results["Easy vs Medium"]["total"] + comparison_results["Medium vs Hard"]["total"]
        
        total_hard_wins = (comparison_results["Medium vs Hard"]["hard"] + 
                          comparison_results["Easy vs Hard"]["hard"])
        total_hard_games = comparison_results["Medium vs Hard"]["total"] + comparison_results["Easy vs Hard"]["total"]
        
        print(f"\n📈 EASY:")
        print(f"   Total: {total_easy_wins}/{total_easy_games} vitórias ({total_easy_wins/total_easy_games*100:.1f}%)")
        print(f"   - vs Medium: {comparison_results['Easy vs Medium']['easy']}/{num_games}")
        print(f"   - vs Hard: {comparison_results['Easy vs Hard']['easy']}/{num_games}")
        
        print(f"\n📈 MEDIUM:")
        print(f"   Total: {total_medium_wins}/{total_medium_games} vitórias ({total_medium_wins/total_medium_games*100:.1f}%)")
        print(f"   - vs Easy: {comparison_results['Easy vs Medium']['medium']}/{num_games}")
        print(f"   - vs Hard: {comparison_results['Medium vs Hard']['medium']}/{num_games}")
        
        print(f"\n📈 HARD:")
        print(f"   Total: {total_hard_wins}/{total_hard_games} vitórias ({total_hard_wins/total_hard_games*100:.1f}%)")
        print(f"   - vs Easy: {comparison_results['Easy vs Hard']['hard']}/{num_games}")
        print(f"   - vs Medium: {comparison_results['Medium vs Hard']['hard']}/{num_games}")
        
        print(f"\n💡 CONCLUSÃO:")
        if total_hard_wins/total_hard_games > total_medium_wins/total_medium_games > total_easy_wins/total_easy_games:
            print("   ✅ Hard > Medium > Easy (como esperado!)")
        elif total_hard_wins/total_hard_games > total_easy_wins/total_easy_games:
            print("   ✅ Hard é mais forte que Easy")
        else:
            print("   ⚠️ Resultados inesperados - pode precisar mais treinamento")
        
        print(f"{'='*60}\n")
        
        return comparison_results
    
    def _play_1v1(self, difficulty1: str, difficulty2: str) -> Optional[str]:
        """Joga uma partida 1v1 entre duas IAs"""
        ai1 = CoupAI(name="IA1", difficulty=difficulty1)
        ai2 = CoupAI(name="IA2", difficulty=difficulty2)
        
        game = CoupGame([ai1.name, ai2.name])
        
        max_turns = 200
        for _ in range(max_turns):
            if game.is_game_over():
                break
            
            current = game.get_current_player()
            if current.eliminated:
                game.next_turn()
                continue
            
            ai = ai1 if current.name == ai1.name else ai2
            
            action, target, is_bluff = ai.choose_action(game, current)
            game.execute_action(action, current, target, is_bluff)
            
            # Reações simples - verifica se há outros jogadores
            other_players = game.get_other_players(current)
            if other_players:
                other = other_players[0]
                other_ai = ai1 if other.name == ai1.name else ai2
                
                if action == Action.FOREIGN_AID:
                    if other_ai.should_block(game, other, action, current):
                        if other.has_card(Character.DUKE) or random.random() < 0.5:
                            current.coins -= 2
                
                # Desafios para ações que podem ser desafiadas
                if action in [Action.TAX, Action.ASSASSINATE, Action.STEAL, Action.EXCHANGE]:
                    if other_ai.should_challenge(game, other, current, action):
                        # Processa desafio
                        if is_bluff:
                            # Blefe descoberto - perde carta
                            if current.cards:
                                current.lose_card(current.cards[0])
                        else:
                            # Desafio falhou - quem desafiou perde carta
                            if other.cards:
                                other.lose_card(other.cards[0])
            
            game.next_turn()
            
            winner = game.get_winner()
            if winner:
                return difficulty1 if winner.name == ai1.name else difficulty2
        
        winner = game.get_winner()
        return difficulty1 if winner and winner.name == ai1.name else difficulty2 if winner else None
    
    def train_with_learning(self, num_games: int = 100):
        """Treina IA com sistema de aprendizado adaptativo PERSISTENTE"""
        print(f"\n{'='*60}")
        print(f"🧠 TREINAMENTO COM APRENDIZADO ADAPTATIVO")
        print(f"{'='*60}")
        
        # Mostra conhecimento prévio
        if self.learning.learning_data["total_games"] > 0:
            prev_win_rate = self.learning.get_win_rate() * 100
            print(f"Conhecimento prévio: {self.learning.learning_data['total_games']} partidas, {prev_win_rate:.1f}% vitórias")
        print(f"{'='*60}\n")
        
        wins = 0
        
        for game_num in range(1, num_games + 1):
            # Carrega parâmetros aprendidos (atualizados a cada partida)
            learned_params = self.learning.get_strategy_params()
            
            # Joga partida individual
            trained_ai = CoupAI(name="IA_Treinada", difficulty="hard", learning_params=learned_params)
            opponents = [
                CoupAI(name="Oponente_1", difficulty="medium"),
                CoupAI(name="Oponente_2", difficulty="easy")
            ]
            
            game = CoupGame([trained_ai.name, opponents[0].name, opponents[1].name])
            winner = self._play_game(game, trained_ai, opponents)
            
            won = winner and winner.name == trained_ai.name
            if won:
                wins += 1
            
            # Aprende com o resultado
            self.learning.record_game_result(won)
            recent_win_rate = self.learning.get_recent_win_rate(10)
            self.learning.learn_from_results(won, recent_win_rate)
            
            # Salva a cada 20 partidas
            if game_num % 20 == 0:
                self.learning.save_learning()
                print(f"\n📈 Progresso: {game_num}/{num_games}")
                print(f"   Vitórias: {wins}/{game_num} ({(wins/game_num)*100:.1f}%)")
                print(f"   Taxa recente: {recent_win_rate*100:.1f}%")
                print(f"   Parâmetros aprendidos:")
                params = self.learning.learning_data['strategy_params']
                print(f"   - Blefe: {params['bluff_probability']:.2f}")
                print(f"   - Desafio: {params['challenge_aggressiveness']:.2f}")
                print(f"   - Bloqueio: {params['block_probability']:.2f}")
        
        # Salva aprendizado final
        self.learning.save_learning()
        
        print(f"\n✅ Aprendizado concluído!")
        print(f"   Taxa de vitória final: {(wins/num_games)*100:.1f}%")
        print(f"   💾 Conhecimento salvo em: {self.learning.LEARNING_FILE}")
        print(f"   Total de partidas (todas sessões): {self.learning.learning_data['total_games']}")
        
        return self.learning.get_strategy_params()

def main_trainer():
    """Menu principal do treinador"""
    trainer = AITrainer()
    
    print("\n" + "🎓" * 30)
    print("SISTEMA DE TREINAMENTO DE IA - COUP")
    print("🎓" * 30)
    print("\nEscolha uma opção:")
    print("1. Treinar IA Hard contra oponentes fáceis")
    print("2. Treinar IA Hard contra oponentes médios")
    print("3. Treinar IA Hard contra mix (fácil + médio)")
    print("4. Comparar níveis de IA (Easy vs Medium vs Hard)")
    print("5. Treinamento com aprendizado adaptativo")
    print("6. Ver estatísticas de aprendizado")
    print("7. Sair")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == "1":
        num = int(input("Quantas partidas? (padrão: 100): ").strip() or "100")
        trainer.train_ai(num, "hard", ["easy", "easy"])
    
    elif choice == "2":
        num = int(input("Quantas partidas? (padrão: 100): ").strip() or "100")
        trainer.train_ai(num, "hard", ["medium", "medium"])
    
    elif choice == "3":
        num = int(input("Quantas partidas? (padrão: 100): ").strip() or "100")
        trainer.train_ai(num, "hard", ["easy", "medium"])
    
    elif choice == "4":
        num = int(input("Quantas partidas por comparação? (padrão: 50): ").strip() or "50")
        trainer.compare_ai_levels(num)
    
    elif choice == "5":
        num = int(input("Quantas partidas? (padrão: 100): ").strip() or "100")
        trainer.train_with_learning(num)
    
    elif choice == "6":
        trainer.learning.print_stats()
        input("\nPressione Enter para continuar...")
        main_trainer()
    
    elif choice == "7":
        print("Até logo!")
    
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main_trainer()

