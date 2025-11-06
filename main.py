"""
Sistema de IA para jogar e vencer Coup
Interface principal do jogo
"""
import os
from coup_game import CoupGame, Player, Action, Character
from coup_ai import CoupAI
from coup_assistant import CoupAssistant

def print_header():
    """Imprime cabeçalho do jogo"""
    print("=" * 60)
    print(" " * 15 + "🎮 COUP - IA ASSISTENTE 🎮")
    print("=" * 60)
    print()

def print_game_state(game: CoupGame, human_player: Player):
    """Mostra o estado atual do jogo"""
    print("\n" + "=" * 60)
    print("ESTADO DO JOGO")
    print("=" * 60)
    
    state = game.get_game_state(human_player)
    
    print(f"\n📊 Suas informações:")
    print(f"   Moedas: {human_player.coins}")
    print(f"   Cartas: {len(human_player.cards)}")
    print(f"   Suas cartas: {', '.join([c.value for c in human_player.cards])}")
    
    print(f"\n👥 Outros jogadores:")
    for p_info in state["players"]:
        if p_info["name"] != human_player.name:
            print(f"   {p_info['name']}: {p_info['coins']} moedas, {p_info['cards_count']} carta(s)", end="")
            if p_info["eliminated"]:
                print(" [ELIMINADO]")
            else:
                print()
    
    print(f"\n📚 Baralho: {state['deck_size']} cartas restantes")
    print("=" * 60)

def get_action_from_user() -> Action:
    """Pede ação ao usuário"""
    print("\n📋 Ações disponíveis:")
    print("1. Income (ganha 1 moeda)")
    print("2. Foreign Aid (ganha 2 moedas, pode ser bloqueado)")
    print("3. Tax (Duque - ganha 3 moedas)")
    print("4. Assassinar (Assassino - paga 3, elimina carta)")
    print("5. Roubar (Capitão - rouba 2 moedas)")
    print("6. Trocar (Embaixador - troca cartas)")
    print("7. Coup (paga 7 moedas, elimina carta)")
    
    while True:
        choice = input("\nEscolha uma ação (1-7): ").strip()
        
        action_map = {
            "1": Action.INCOME,
            "2": Action.FOREIGN_AID,
            "3": Action.TAX,
            "4": Action.ASSASSINATE,
            "5": Action.STEAL,
            "6": Action.EXCHANGE,
            "7": Action.COUP
        }
        
        if choice in action_map:
            return action_map[choice]
        print("❌ Opção inválida! Escolha de 1 a 7.")

def get_target_from_user(game: CoupGame, player: Player) -> Player:
    """Pede alvo ao usuário"""
    other_players = game.get_other_players(player)
    
    if not other_players:
        return None
    
    print("\n👥 Escolha um alvo:")
    for i, target in enumerate(other_players, 1):
        print(f"{i}. {target.name} ({target.coins} moedas, {len(target.cards)} carta(s))")
    
    while True:
        choice = input("\nEscolha um alvo: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(other_players):
                return other_players[idx]
            print("❌ Opção inválida!")
        except ValueError:
            print("❌ Digite um número válido!")

def ask_bluff() -> bool:
    """Pergunta se o jogador está blefando"""
    while True:
        response = input("\nVocê está blefando? (s/n): ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            return True
        elif response in ['n', 'não', 'nao', 'no']:
            return False
        print("❌ Digite 's' para sim ou 'n' para não.")

def handle_challenge(game: CoupGame, challenger: Player, target: Player, 
                    action: Action, was_bluff: bool):
    """Processa um desafio"""
    print(f"\n⚔️ {challenger.name} desafiou {target.name}!")
    
    if was_bluff:
        # Blefe foi descoberto!
        print(f"❌ {target.name} estava blefando!")
        if target.cards:
            card = target.cards[0]
            eliminated = target.lose_card(card)
            print(f"   {target.name} perdeu {card.value}!")
            if eliminated:
                print(f"   {target.name} foi ELIMINADO!")
    else:
        # Desafio falhou!
        print(f"✅ {target.name} tinha a carta!")
        if challenger.cards:
            card = challenger.cards[0]
            eliminated = challenger.lose_card(card)
            print(f"   {challenger.name} perdeu {card.value} por desafiar incorretamente!")
            if eliminated:
                print(f"   {challenger.name} foi ELIMINADO!")

def play_with_assistant():
    """Modo: Jogador humano com assistente de IA"""
    print_header()
    print("🤖 MODO: Jogador com Assistente de IA")
    print("\nVocê jogará contra IAs, mas terá um assistente que te ajuda a vencer!")
    print()
    
    player_name = input("Digite seu nome: ").strip() or "Você"
    num_opponents = int(input("Quantos oponentes IA? (1-3): ").strip() or "2")
    
    # Cria jogo
    names = [player_name] + [f"IA{i+1}" for i in range(num_opponents)]
    game = CoupGame(names)
    
    # Cria IAs e assistente
    ais = [CoupAI(name=f"IA{i+1}", difficulty="hard") for i in range(num_opponents)]
    assistant = CoupAssistant()
    
    human_player = game.players[0]
    
    print(f"\n✅ Jogo iniciado! Você tem {len(human_player.cards)} cartas e {human_player.coins} moedas.")
    input("\nPressione Enter para começar...")
    
    round_num = 1
    
    while not game.is_game_over():
        print(f"\n{'='*60}")
        print(f"ROUND {round_num}")
        print(f"{'='*60}")
        
        current = game.get_current_player()
        
        if current == human_player:
            # Turno do jogador humano
            print_game_state(game, human_player)
            
            # Assistente dá recomendação
            print("\n" + "🤖" * 30)
            print("ASSISTENTE DE IA")
            print("🤖" * 30)
            recommendation = assistant.get_recommendation(game, human_player)
            
            print(f"\n💡 Recomendação: {recommendation['best_action'].value}")
            if recommendation['target']:
                print(f"   Alvo: {recommendation['target'].name}")
            print(f"   Confiança: {recommendation['confidence']*100:.0f}%")
            print(f"   Motivo: {recommendation['reasoning']}")
            
            if recommendation['warnings']:
                print(f"\n⚠️ Avisos:")
                for warning in recommendation['warnings']:
                    print(f"   - {warning}")
            
            if recommendation['tips']:
                print(f"\n💡 Dicas:")
                for tip in recommendation['tips']:
                    print(f"   - {tip}")
            
            # Pergunta se quer seguir recomendação
            follow = input("\nSeguir recomendação? (s/n): ").strip().lower()
            
            if follow == 's':
                action = recommendation['best_action']
                target = recommendation['target']
                is_bluff = recommendation['should_bluff']
            else:
                # Pede ação manual
                action = get_action_from_user()
                target = None
                is_bluff = False
                
                if action in [Action.COUP, Action.ASSASSINATE, Action.STEAL]:
                    target = get_target_from_user(game, human_player)
                
                if action in [Action.TAX, Action.STEAL, Action.ASSASSINATE]:
                    is_bluff = ask_bluff()
            
            # Executa ação
            result = game.execute_action(action, human_player, target, is_bluff)
            print(f"\n{result['message']}")
            
            # Outros jogadores podem desafiar/bloquear
            for ai_player in game.get_other_players(human_player):
                if action == Action.FOREIGN_AID:
                    if ai_player.has_card(Character.DUKE) or (ai_player.name.startswith("IA") and 
                        CoupAI(name=ai_player.name).should_block(game, ai_player, action, human_player)):
                        print(f"{ai_player.name} bloqueou Foreign Aid com Duque!")
                        human_player.coins -= 2
                
                elif action == Action.STEAL and target == ai_player:
                    should_block = ai_player.has_card(Character.CAPTAIN) or ai_player.has_card(Character.AMBASSADOR)
                    if should_block:
                        print(f"{ai_player.name} bloqueou o roubo!")
                        # Não rouba
                    elif ai_player.name.startswith("IA"):
                        ai = next(a for a in ais if a.name == ai_player.name)
                        if ai.should_challenge(game, ai_player, human_player, action):
                            handle_challenge(game, ai_player, human_player, action, is_bluff)
            
            game.next_turn()
            
        else:
            # Turno da IA
            print(f"\n🎯 Turno de {current.name}")
            ai = next((a for a in ais if a.name == current.name), None)
            
            if ai:
                action, target, is_bluff = ai.choose_action(game, current)
                print(f"{current.name} escolheu: {action.value}")
                if target:
                    print(f"   Alvo: {target.name}")
                
                result = game.execute_action(action, current, target, is_bluff)
                print(f"{result['message']}")
                
                # Jogador humano pode desafiar/bloquear
                if action == Action.FOREIGN_AID:
                    should_block, reasoning = assistant.should_block_action(game, human_player, action, current)
                    if should_block:
                        print(f"\n💡 Assistente recomenda: {reasoning}")
                        block = input("Bloquear? (s/n): ").strip().lower()
                        if block == 's' and human_player.has_card(Character.DUKE):
                            print(f"Você bloqueou Foreign Aid com Duque!")
                            current.coins -= 2
                
                elif action == Action.STEAL and target == human_player:
                    should_block, reasoning = assistant.should_block_action(game, human_player, action, current)
                    if should_block and (human_player.has_card(Character.CAPTAIN) or 
                                         human_player.has_card(Character.AMBASSADOR)):
                        print(f"\n💡 Assistente recomenda: {reasoning}")
                        block = input("Bloquear? (s/n): ").strip().lower()
                        if block == 's':
                            print(f"Você bloqueou o roubo!")
                    else:
                        should_challenge, reasoning = assistant.should_challenge_action(game, human_player, current, action)
                        if should_challenge:
                            print(f"\n💡 Assistente recomenda: {reasoning}")
                            challenge = input("Desafiar? (s/n): ").strip().lower()
                            if challenge == 's':
                                handle_challenge(game, human_player, current, action, is_bluff)
            
            game.next_turn()
        
        # Verifica fim de jogo
        winner = game.get_winner()
        if winner:
            print(f"\n{'='*60}")
            print(f"🏆 {winner.name} VENCEU!")
            print(f"{'='*60}")
            break
        
        round_num += 1

def main():
    """Menu principal"""
    print_header()
    print("Escolha um modo:")
    print("1. Jogar no Computador com Assistente de IA")
    print("2. 🎮 Assistente para JOGO FÍSICO (recomendado!)")
    print("3. 🎓 Treinar IA (IA vs IA)")
    print("4. Sair")
    
    choice = input("\nEscolha: ").strip()
    
    if choice == "1":
        play_with_assistant()
    elif choice == "2":
        from physical_game_assistant import main_physical
        main_physical()
    elif choice == "3":
        from ai_trainer import main_trainer
        main_trainer()
    elif choice == "4":
        print("Até logo!")
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()