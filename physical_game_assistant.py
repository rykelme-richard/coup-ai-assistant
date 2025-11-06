"""
Assistente de IA para jogar Coup FÍSICO com amigos
Você informa o estado do jogo e recebe recomendações
"""
from typing import List, Dict, Optional
from coup_assistant import CoupAssistant
from coup_game import CoupGame, Player, Action, Character

class PhysicalGameAssistant:
    """Assistente para jogo físico - você informa o estado e recebe ajuda"""
    
    def __init__(self):
        self.assistant = CoupAssistant()
        self.game_state = {
            "your_name": "",
            "your_coins": 2,
            "your_cards": [],
            "opponents": [],  # [{"name": str, "coins": int, "cards_count": int}]
            "deck_size": 15  # 15 cartas no baralho (3 de cada personagem)
        }
        self.turn_order = []  # Ordem de jogada
        self.current_turn_index = 0  # Índice do jogador atual
        self.rounds = []  # Histórico de rodadas
        self.first_player = ""  # Quem começou
        
    def setup_game(self):
        """Configura o jogo inicial"""
        print("\n" + "=" * 60)
        print("🤖 CONFIGURAÇÃO DO ASSISTENTE PARA JOGO FÍSICO")
        print("=" * 60)
        
        self.game_state["your_name"] = input("\nSeu nome: ").strip() or "Você"
        
        print("\n📋 Suas cartas:")
        print("1. Duque")
        print("2. Assassino")
        print("3. Capitão")
        print("4. Embaixador")
        print("5. Condessa")
        
        cards = []
        for i in range(2):
            while True:
                choice = input(f"\nCarta {i+1} (1-5): ").strip()
                card_map = {
                    "1": Character.DUKE,
                    "2": Character.ASSASSIN,
                    "3": Character.CAPTAIN,
                    "4": Character.AMBASSADOR,
                    "5": Character.CONTESSA
                }
                if choice in card_map:
                    cards.append(card_map[choice])
                    print(f"✅ {card_map[choice].value} adicionado")
                    break
                print("❌ Opção inválida!")
        
        self.game_state["your_cards"] = cards
        
        # Pergunta sobre oponentes
        num_opponents = int(input("\nQuantos oponentes? ").strip() or "2")
        
        for i in range(num_opponents):
            name = input(f"\nNome do oponente {i+1}: ").strip()
            coins = int(input(f"Moedas de {name}: ").strip() or "2")
            cards_count = int(input(f"Cartas de {name} (visíveis): ").strip() or "2")
            
            self.game_state["opponents"].append({
                "name": name,
                "coins": coins,
                "cards_count": cards_count
            })
        
        # Configura ordem de jogada
        print("\n" + "=" * 60)
        print("📋 CONFIGURAÇÃO DA ORDEM DE JOGADA")
        print("=" * 60)
        
        all_players = [self.game_state["your_name"]] + [opp["name"] for opp in self.game_state["opponents"]]
        
        print("\nJogadores:")
        for i, name in enumerate(all_players, 1):
            print(f"  {i}. {name}")
        
        # Pergunta quem começou
        print("\nQuem começou a jogada?")
        while True:
            first_name = input("Nome do jogador que começou: ").strip()
            if first_name in all_players:
                self.first_player = first_name
                break
            print("❌ Nome não encontrado! Digite um nome válido.")
        
        # Define ordem de jogada começando pelo primeiro
        first_index = all_players.index(self.first_player)
        self.turn_order = all_players[first_index:] + all_players[:first_index]
        
        # Mostra ordem de jogada
        print("\n" + "=" * 60)
        print("✅ CONFIGURAÇÃO COMPLETA!")
        print("=" * 60)
        print(f"\nQUEM COMEÇOU A JOGADA: {self.first_player}")
        print("\nOrdem de jogada:")
        for i, name in enumerate(self.turn_order, 1):
            print(f"  Ordem de jogada {i}: {name}")
        
        print(f"\n📊 Estado inicial:")
        print(f"  {self.game_state['your_name']}: {len(self.game_state['your_cards'])} cartas, {self.game_state['your_coins']} moedas")
        for opp in self.game_state["opponents"]:
            print(f"  {opp['name']}: {opp['cards_count']} cartas, {opp['coins']} moedas")
        
        self.current_turn_index = 0
    
    def update_state(self):
        """Atualiza o estado do jogo"""
        print("\n" + "=" * 60)
        print("🔄 ATUALIZAR ESTADO DO JOGO")
        print("=" * 60)
        
        # Atualiza suas moedas
        new_coins = input(f"\nSuas moedas (atual: {self.game_state['your_coins']}): ").strip()
        if new_coins:
            self.game_state["your_coins"] = int(new_coins)
        
        # Atualiza cartas (se perdeu alguma)
        if len(self.game_state["your_cards"]) > 1:
            lost = input("Você perdeu alguma carta? (nome da carta ou Enter): ").strip()
            if lost:
                for char in Character:
                    if char.value.lower() == lost.lower():
                        if char in self.game_state["your_cards"]:
                            self.game_state["your_cards"].remove(char)
                            print(f"✅ {char.value} removido")
                            break
        
        # Atualiza oponentes
        for opp in self.game_state["opponents"]:
            print(f"\n{opp['name']}:")
            new_coins = input(f"  Moedas (atual: {opp['coins']}): ").strip()
            if new_coins:
                opp["coins"] = int(new_coins)
            
            new_cards = input(f"  Cartas visíveis (atual: {opp['cards_count']}): ").strip()
            if new_cards:
                opp["cards_count"] = int(new_cards)
    
    def get_recommendation(self):
        """Obtém recomendação baseada no estado atual"""
        # Cria um jogo simulado para usar o assistente
        game = self._create_simulated_game()
        player = game.players[0]
        
        # Atualiza moedas do jogador
        player.coins = self.game_state["your_coins"]
        
        print("\n" + "🤖" * 30)
        print("ASSISTENTE ANALISANDO...")
        print("🤖" * 30)
        
        recommendation = self.assistant.get_recommendation(game, player)
        
        print("\n" + "=" * 60)
        print("💡 RECOMENDAÇÃO DO ASSISTENTE")
        print("=" * 60)
        
        # Mostra análise do Gemini se disponível
        if recommendation.get('gemini_analysis'):
            print("\n" + "✨" * 30)
            print("ANÁLISE AVANÇADA (Gemini AI)")
            print("✨" * 30)
            print(recommendation['gemini_analysis'])
            print("=" * 60)
        
        print(f"\n🎯 Melhor Ação: {recommendation['best_action'].value.upper()}")
        if recommendation['target']:
            print(f"🎯 Alvo: {recommendation['target'].name}")
        
        print(f"📊 Confiança: {recommendation['confidence']*100:.0f}%")
        
        print(f"\n💭 Motivo:")
        print(f"   {recommendation['reasoning']}")
        
        if recommendation['warnings']:
            print(f"\n⚠️ Avisos:")
            for warning in recommendation['warnings']:
                print(f"   • {warning}")
        
        if recommendation['tips']:
            print(f"\n💡 Dicas:")
            for tip in recommendation['tips']:
                print(f"   • {tip}")
        
        if recommendation['alternatives']:
            print(f"\n🔄 Alternativas:")
            for alt in recommendation['alternatives']:
                print(f"   • {alt['action'].value}: {alt['reasoning']}")
        
        print("\n" + "=" * 60)
        
        return recommendation
    
    def _create_simulated_game(self):
        """Cria um jogo simulado para análise"""
        names = [self.game_state["your_name"]] + [opp["name"] for opp in self.game_state["opponents"]]
        game = CoupGame(names)
        
        # Define suas cartas
        game.players[0].cards = self.game_state["your_cards"].copy()
        game.players[0].coins = self.game_state["your_coins"]
        
        # Define estado dos oponentes (aproximado)
        for i, opp_info in enumerate(self.game_state["opponents"]):
            player = game.players[i + 1]
            player.coins = opp_info["coins"]
            # Não sabemos as cartas exatas, mas sabemos quantas tem
            # Mantém as cartas que já foram distribuídas
        
        return game
    
    def analyze_action(self, action_name: str, actor_name: str, target_name: Optional[str] = None):
        """Analisa uma ação que está acontecendo no jogo"""
        print("\n" + "=" * 60)
        print(f"🔍 ANALISANDO AÇÃO: {action_name.upper()}")
        print("=" * 60)
        
        # Mapeia nome da ação
        action_map = {
            "income": Action.INCOME,
            "foreign aid": Action.FOREIGN_AID,
            "foreign_aid": Action.FOREIGN_AID,
            "tax": Action.TAX,
            "assassinar": Action.ASSASSINATE,
            "assassinate": Action.ASSASSINATE,
            "roubar": Action.STEAL,
            "steal": Action.STEAL,
            "trocar": Action.EXCHANGE,
            "exchange": Action.EXCHANGE,
            "coup": Action.COUP
        }
        
        action = action_map.get(action_name.lower())
        if not action:
            print(f"❌ Ação '{action_name}' não reconhecida")
            return
        
        # Cria jogo simulado
        game = self._create_simulated_game()
        player = game.players[0]
        
        # Encontra o ator
        actor = None
        if actor_name == self.game_state["your_name"]:
            actor = player
        else:
            for p in game.players:
                if p.name == actor_name:
                    actor = p
                    break
        
        if not actor:
            print(f"❌ Jogador '{actor_name}' não encontrado")
            return
        
        # Encontra alvo se necessário
        target = None
        if target_name:
            if target_name == self.game_state["your_name"]:
                target = player
            else:
                for p in game.players:
                    if p.name == target_name:
                        target = p
                        break
        
        # Se é contra você, analisa defesa
        if target == player:
            print(f"\n⚠️ {actor_name} está atacando VOCÊ!")
            
            if action == Action.FOREIGN_AID:
                should_block, reasoning = self.assistant.should_block_action(game, player, action, actor)
                print(f"\n💡 Recomendação: {reasoning}")
                if should_block and player.has_card(Character.DUKE):
                    print("✅ Você pode bloquear com Duque!")
                elif not player.has_card(Character.DUKE):
                    print("❌ Você não pode bloquear (não tem Duque)")
            
            elif action == Action.STEAL:
                should_block, reasoning = self.assistant.should_block_action(game, player, action, actor)
                print(f"\n💡 Recomendação: {reasoning}")
                if should_block and (player.has_card(Character.CAPTAIN) or player.has_card(Character.AMBASSADOR)):
                    print("✅ Você pode bloquear com Capitão ou Embaixador!")
                else:
                    should_challenge, challenge_reasoning = self.assistant.should_challenge_action(game, player, actor, action)
                    print(f"\n💡 Desafiar: {challenge_reasoning}")
            
            elif action == Action.ASSASSINATE:
                should_block, reasoning = self.assistant.should_block_action(game, player, action, actor)
                print(f"\n💡 Recomendação: {reasoning}")
                if should_block and player.has_card(Character.CONTESSA):
                    print("✅ Você pode bloquear com Condessa!")
                else:
                    print("❌ Você não pode bloquear (não tem Condessa)")
                    print("⚠️ Você vai perder uma carta se não bloquear!")
        
        # Se você está fazendo a ação, analisa se deve desafiar
        if actor == player:
            print(f"\n✅ Você está fazendo: {action.value}")
            print("💡 Outros jogadores podem desafiar você")
            
            # Verifica se você tem a carta
            has_card = False
            if action == Action.TAX:
                has_card = player.has_card(Character.DUKE)
            elif action == Action.ASSASSINATE:
                has_card = player.has_card(Character.ASSASSIN)
            elif action == Action.STEAL:
                has_card = player.has_card(Character.CAPTAIN)
            elif action == Action.EXCHANGE:
                has_card = player.has_card(Character.AMBASSADOR)
            
            if has_card:
                print("✅ Você tem a carta! Se desafiarem, quem desafiou perde uma carta.")
            else:
                print("⚠️ Você está BLEFANDO! Se desafiarem, você perde uma carta.")
        
        # Se outro jogador está fazendo, analisa desafio
        elif actor != player:
            should_challenge, reasoning = self.assistant.should_challenge_action(game, player, actor, action)
            print(f"\n💡 Desafiar {actor_name}?")
            print(f"   {reasoning}")
            
            if should_challenge:
                print("✅ Recomendação: DESAFIE!")
                print("   Mas considere: você pode perder uma carta se ele tiver a carta.")
            else:
                print("❌ Recomendação: NÃO desafie")
                print("   A ação não é crítica ou o risco é alto.")
    
    def get_current_player_name(self) -> str:
        """Retorna o nome do jogador atual"""
        if self.current_turn_index < len(self.turn_order):
            return self.turn_order[self.current_turn_index]
        return ""
    
    def next_turn(self):
        """Avança para o próximo turno"""
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
    
    def register_round(self, player_name: str, action_description: str):
        """
        Registra uma rodada de um jogador
        
        Args:
            player_name: Nome do jogador
            action_description: Descrição do que aconteceu (ex: "pegou 2 moedas", "foi bloqueado pela Joana")
        """
        round_entry = {
            "player": player_name,
            "action": action_description
        }
        self.rounds.append(round_entry)
        
        # Mostra a rodada registrada no formato solicitado
        print(f"\n{'='*60}")
        print(f"Rodada do {player_name}: {action_description}")
        print(f"{'='*60}")
    
    def show_round_history(self):
        """Mostra o histórico de rodadas"""
        if not self.rounds:
            print("\n📋 Nenhuma rodada registrada ainda.")
            return
        
        print("\n" + "=" * 60)
        print("📋 HISTÓRICO DE RODADAS")
        print("=" * 60)
        for i, round_entry in enumerate(self.rounds, 1):
            print(f"\n{i}. Rodada do {round_entry['player']}: {round_entry['action']}")
        print("=" * 60)
    
    def interactive_mode(self):
        """Modo interativo para registrar rodadas"""
        print("\n" + "=" * 60)
        print("🎮 MODO RODADAS - JOGO FÍSICO")
        print("=" * 60)
        print("\nComandos disponíveis:")
        print("  'rodada' ou 'r' - Registrar rodada do jogador atual")
        print("  'historico' ou 'h' - Ver histórico de rodadas")
        print("  'ajuda' - Recebe recomendação da IA")
        print("  'atualizar' ou 'u' - Atualiza estado do jogo")
        print("  'proximo' ou 'p' - Avança para próximo jogador")
        print("  'sair' ou 'quit' - Sair")
        
        while True:
            current_player = self.get_current_player_name()
            print("\n" + "-" * 60)
            print(f"🎯 Jogador atual: {current_player}")
            print("-" * 60)
            command = input("\n💬 Comando: ").strip().lower()
            
            if command in ['sair', 'quit', 'exit']:
                print("👋 Até logo!")
                break
            
            elif command in ['rodada', 'r']:
                self._register_round_interactive()
            
            elif command in ['historico', 'h', 'histórico']:
                self.show_round_history()
            
            elif command in ['ajuda', 'help']:
                self.get_recommendation()
            
            elif command in ['atualizar', 'update', 'u']:
                self.update_state()
            
            elif command in ['proximo', 'p', 'próximo']:
                self.next_turn()
                print(f"✅ Próximo jogador: {self.get_current_player_name()}")
            
            else:
                print("❌ Comando não reconhecido. Digite 'help' para ver comandos.")
    
    def _get_recommendations_for_action(self, action_choice: str, actor_name: str, target_name: str = None):
        """
        Gera recomendações para o jogador principal quando outro jogador faz uma ação
        
        Args:
            action_choice: Escolha da ação (1-7)
            actor_name: Nome do jogador que fez a ação
            target_name: Nome do alvo (se houver)
        """
        your_name = self.game_state["your_name"]
        your_cards = self.game_state["your_cards"]
        
        # Mapeia escolha para Action primeiro para verificar tipo
        action_map = {
            "1": Action.INCOME,
            "2": Action.FOREIGN_AID,
            "3": Action.TAX,
            "4": Action.ASSASSINATE,
            "5": Action.STEAL,
            "6": Action.EXCHANGE,
            "7": Action.COUP
        }
        
        action = action_map.get(action_choice)
        if not action:
            return None
        
        # Se a ação tem alvo específico e não é você, não precisa de recomendação
        if target_name and target_name != your_name and action != Action.FOREIGN_AID:
            return None
        
        recommendations = []
        
        # Se você é o alvo ou a ação afeta você, dá recomendações de defesa
        is_target = target_name == your_name
        is_foreign_aid = action == Action.FOREIGN_AID and actor_name != your_name
        
        if is_target or is_foreign_aid:
            if action == Action.FOREIGN_AID:
                if Character.DUKE in your_cards:
                    recommendations.append({
                        "type": "block",
                        "message": f"✅ BLOQUEIE! Você tem Duque. Use: 'Bloqueio Foreign Aid com Duque'",
                        "card": "Duque"
                    })
                else:
                    recommendations.append({
                        "type": "bluff",
                        "message": f"💡 BLEFE! Minta e bloqueie dizendo que você tem Duque. Use: 'Bloqueio Foreign Aid com Duque'",
                        "card": "Duque"
                    })
            
            elif action == Action.STEAL:
                if Character.CAPTAIN in your_cards:
                    recommendations.append({
                        "type": "block",
                        "message": f"✅ BLOQUEIE! Você tem Capitão. Use: 'Bloqueio roubo com Capitão'",
                        "card": "Capitão"
                    })
                elif Character.AMBASSADOR in your_cards:
                    recommendations.append({
                        "type": "block",
                        "message": f"✅ BLOQUEIE! Você tem Embaixador. Use: 'Bloqueio roubo com Embaixador'",
                        "card": "Embaixador"
                    })
                else:
                    recommendations.append({
                        "type": "bluff",
                        "message": f"💡 BLEFE! Minta e bloqueie dizendo que você tem Capitão ou Embaixador. Use: 'Bloqueio roubo com Capitão'",
                        "card": "Capitão"
                    })
                    recommendations.append({
                        "type": "challenge",
                        "message": f"⚔️ DESAFIE! Se você acha que {actor_name} não tem Capitão, desafie a ação.",
                        "card": None
                    })
            
            elif action == Action.ASSASSINATE:
                if Character.CONTESSA in your_cards:
                    recommendations.append({
                        "type": "block",
                        "message": f"✅ BLOQUEIE! Você tem Condessa. Use: 'Bloqueio assassinato com Condessa'",
                        "card": "Condessa"
                    })
                else:
                    recommendations.append({
                        "type": "bluff",
                        "message": f"💡 BLEFE! Minta e bloqueie dizendo que você tem Condessa. Use: 'Bloqueio assassinato com Condessa'",
                        "card": "Condessa"
                    })
                    recommendations.append({
                        "type": "warning",
                        "message": f"⚠️ ATENÇÃO! Se não bloquear (ou blefar), você perderá uma carta!",
                        "card": None
                    })
            
            elif action == Action.COUP:
                recommendations.append({
                    "type": "warning",
                    "message": f"⚠️ Coup não pode ser bloqueado ou desafiado. Você vai perder uma carta!",
                    "card": None
                })
        
        # Se você não é o alvo e a ação não é Foreign Aid, dá recomendações de desafio
        elif actor_name != your_name and action != Action.FOREIGN_AID:
            if action == Action.TAX:
                recommendations.append({
                    "type": "challenge",
                    "message": f"⚔️ DESAFIE! Se você acha que {actor_name} não tem Duque, desafie a ação Tax.",
                    "card": "Duque"
                })
            elif action == Action.ASSASSINATE:
                recommendations.append({
                    "type": "challenge",
                    "message": f"⚔️ DESAFIE! Se você acha que {actor_name} não tem Assassino, desafie a ação.",
                    "card": "Assassino"
                })
            elif action == Action.STEAL:
                recommendations.append({
                    "type": "challenge",
                    "message": f"⚔️ DESAFIE! Se você acha que {actor_name} não tem Capitão, desafie a ação de roubo.",
                    "card": "Capitão"
                })
            elif action == Action.EXCHANGE:
                recommendations.append({
                    "type": "challenge",
                    "message": f"⚔️ DESAFIE! Se você acha que {actor_name} não tem Embaixador, desafie a ação de troca.",
                    "card": "Embaixador"
                })
        
        return recommendations
    
    def _show_recommendations(self, recommendations):
        """Mostra as recomendações de forma formatada"""
        if not recommendations:
            return
        
        print("\n" + "=" * 60)
        print("💡 RECOMENDAÇÕES PARA VOCÊ")
        print("=" * 60)
        
        for rec in recommendations:
            print(f"\n{rec['message']}")
        
        print("=" * 60)
    
    def _register_round_interactive(self):
        """Registra uma rodada de forma interativa"""
        current_player = self.get_current_player_name()
        your_name = self.game_state["your_name"]
        
        print(f"\n📝 Registrando rodada do {current_player}")
        print("\nAções disponíveis:")
        print("  1. Income (pegou 1 moeda)")
        print("  2. Foreign Aid (pegou 2 moedas)")
        print("  3. Tax (Duque - pegou 3 moedas)")
        print("  4. Assassinar (Assassino - pagou 3, eliminou carta)")
        print("  5. Roubar (Capitão - roubou 2 moedas)")
        print("  6. Trocar (Embaixador - trocou cartas)")
        print("  7. Coup (pagou 7 moedas, eliminou carta)")
        print("  8. Outra ação (descrever manualmente)")
        
        choice = input("\nEscolha uma ação (1-8): ").strip()
        
        action_descriptions = {
            "1": "pegou 1 moeda",
            "2": "pegou 2 moedas",
            "3": "pegou 3 moedas (Tax - Duque)",
            "4": "assassinou",
            "5": "roubou 2 moedas",
            "6": "trocou cartas",
            "7": "fez Coup"
        }
        
        if choice in action_descriptions:
            description = action_descriptions[choice]
            target_name = None
            
            # Para ações que precisam de alvo, pergunta o alvo
            if choice in ["4", "5", "7"]:  # Assassinar, Roubar, Coup
                target = input("Alvo da ação (ou Enter se não aplicável): ").strip()
                if target:
                    target_name = target
                    description += f" ({target})"
            
            # Se outro jogador fez uma ação, mostra recomendações ANTES de perguntar sobre bloqueio/desafio
            if current_player != your_name:
                recommendations = self._get_recommendations_for_action(choice, current_player, target_name)
                if recommendations:
                    self._show_recommendations(recommendations)
            
            # Pergunta se foi bloqueado/desafiado
            blocked = input("\nFoi bloqueado? (s/n): ").strip().lower()
            if blocked in ['s', 'sim', 'y', 'yes']:
                blocker = input("Quem bloqueou? ").strip()
                description += f", mas foi bloqueado por {blocker}"
            
            challenged = input("Foi desafiado? (s/n): ").strip().lower()
            if challenged in ['s', 'sim', 'y', 'yes']:
                challenger = input("Quem desafiou? ").strip()
                had_card = input("Tinha a carta? (s/n): ").strip().lower()
                if had_card in ['s', 'sim', 'y', 'yes']:
                    description += f", foi desafiado por {challenger}, mas tinha a carta"
                else:
                    # Pergunta qual carta estava blefando
                    card_bluff = input("Qual carta estava blefando? (Duque/Assassino/Capitão/Embaixador): ").strip()
                    description += f", foi desafiado por {challenger}, não tinha {card_bluff}"
            
            self.register_round(current_player, description)
            self.next_turn()
        
        elif choice == "8":
            description = input("Descreva a ação: ").strip()
            self.register_round(current_player, description)
            self.next_turn()
        
        else:
            print("❌ Opção inválida!")

def main_physical():
    """Função principal para modo jogo físico"""
    assistant = PhysicalGameAssistant()
    
    print("\n" + "🎮" * 30)
    print("ASSISTENTE DE IA PARA COUP FÍSICO")
    print("🎮" * 30)
    print("\nEste assistente te ajuda quando você joga Coup FÍSICO com amigos!")
    print("Registre as rodadas conforme o jogo acontece e receba recomendações.")
    
    assistant.setup_game()
    
    print("\n✅ Pronto para começar!")
    print("Use 'rodada' para registrar cada jogada conforme acontece.")
    print("O sistema seguirá a ordem de jogada automaticamente.")
    
    assistant.interactive_mode()

if __name__ == "__main__":
    main_physical()
