"""
Sistema de Aprendizado Persistente para IA de Coup
Salva e carrega conhecimento aprendido entre sessões
"""
import json
import os
from typing import Dict, List
from datetime import datetime

class AILearning:
    """Gerencia aprendizado persistente da IA"""
    
    LEARNING_FILE = "ai_learning.json"
    
    def __init__(self):
        self.learning_data = self._load_learning()
    
    def _load_learning(self) -> Dict:
        """Carrega conhecimento aprendido de arquivo"""
        if os.path.exists(self.LEARNING_FILE):
            try:
                with open(self.LEARNING_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Conhecimento carregado: {data.get('total_games', 0)} partidas")
                    return data
            except Exception as e:
                print(f"⚠️ Erro ao carregar aprendizado: {e}")
        
        # Dados iniciais
        return {
            "total_games": 0,
            "total_wins": 0,
            "total_losses": 0,
            "win_rate_history": [],
            "strategy_params": {
                "bluff_probability": 0.4,
                "challenge_aggressiveness": 0.5,
                "block_probability": 0.7,
                "tax_preference": 0.8,
                "steal_preference": 0.6,
                "assassinate_preference": 0.5
            },
            "action_success_rates": {
                "tax": {"success": 0, "attempts": 0},
                "steal": {"success": 0, "attempts": 0},
                "assassinate": {"success": 0, "attempts": 0},
                "bluff_tax": {"success": 0, "attempts": 0},
                "bluff_steal": {"success": 0, "attempts": 0}
            },
            "opponent_patterns": {},
            "best_strategies": [],
            "last_updated": None
        }
    
    def save_learning(self):
        """Salva conhecimento aprendido em arquivo"""
        self.learning_data["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.LEARNING_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar aprendizado: {e}")
            return False
    
    def record_game_result(self, won: bool):
        """Registra resultado de uma partida"""
        self.learning_data["total_games"] += 1
        if won:
            self.learning_data["total_wins"] += 1
        else:
            self.learning_data["total_losses"] += 1
        
        # Calcula taxa de vitória atual
        if self.learning_data["total_games"] > 0:
            current_win_rate = self.learning_data["total_wins"] / self.learning_data["total_games"]
            self.learning_data["win_rate_history"].append({
                "game": self.learning_data["total_games"],
                "win_rate": current_win_rate
            })
            
            # Mantém apenas últimos 100 registros
            if len(self.learning_data["win_rate_history"]) > 100:
                self.learning_data["win_rate_history"] = self.learning_data["win_rate_history"][-100:]
    
    def update_strategy_params(self, new_params: Dict):
        """Atualiza parâmetros de estratégia aprendidos"""
        for key, value in new_params.items():
            if key in self.learning_data["strategy_params"]:
                # Atualiza gradualmente (média ponderada)
                old_value = self.learning_data["strategy_params"][key]
                # 70% do valor antigo + 30% do novo (aprendizado gradual)
                self.learning_data["strategy_params"][key] = old_value * 0.7 + value * 0.3
    
    def record_action_result(self, action: str, was_successful: bool, was_bluff: bool = False):
        """Registra resultado de uma ação"""
        action_key = action.lower()
        if was_bluff:
            action_key = f"bluff_{action_key}"
        
        if action_key in self.learning_data["action_success_rates"]:
            self.learning_data["action_success_rates"][action_key]["attempts"] += 1
            if was_successful:
                self.learning_data["action_success_rates"][action_key]["success"] += 1
    
    def get_action_success_rate(self, action: str, was_bluff: bool = False) -> float:
        """Retorna taxa de sucesso de uma ação"""
        action_key = action.lower()
        if was_bluff:
            action_key = f"bluff_{action_key}"
        
        if action_key in self.learning_data["action_success_rates"]:
            stats = self.learning_data["action_success_rates"][action_key]
            if stats["attempts"] > 0:
                return stats["success"] / stats["attempts"]
        
        return 0.5  # Taxa padrão se não tem dados
    
    def get_strategy_params(self) -> Dict:
        """Retorna parâmetros de estratégia aprendidos"""
        return self.learning_data["strategy_params"].copy()
    
    def get_win_rate(self) -> float:
        """Retorna taxa de vitória geral"""
        if self.learning_data["total_games"] > 0:
            return self.learning_data["total_wins"] / self.learning_data["total_games"]
        return 0.0
    
    def get_recent_win_rate(self, last_n: int = 20) -> float:
        """Retorna taxa de vitória das últimas N partidas"""
        if len(self.learning_data["win_rate_history"]) < last_n:
            return self.get_win_rate()
        
        recent = self.learning_data["win_rate_history"][-last_n:]
        # Calcula média das taxas recentes
        if recent:
            return sum(w["win_rate"] for w in recent) / len(recent)
        return 0.0
    
    def learn_from_results(self, won: bool, recent_win_rate: float):
        """Aprende e ajusta estratégia baseado em resultados"""
        params = self.learning_data["strategy_params"]
        
        if recent_win_rate < 0.3:
            # Está perdendo muito - precisa ser mais agressivo
            params["bluff_probability"] = min(0.7, params["bluff_probability"] + 0.05)
            params["challenge_aggressiveness"] = min(0.9, params["challenge_aggressiveness"] + 0.05)
        elif recent_win_rate > 0.7:
            # Está ganhando muito - pode ser mais conservador
            params["bluff_probability"] = max(0.2, params["bluff_probability"] - 0.02)
        elif won:
            # Ganhou - mantém estratégia atual (pequeno ajuste positivo)
            params["bluff_probability"] = min(0.6, params["bluff_probability"] + 0.01)
        else:
            # Perdeu - pequeno ajuste negativo
            params["bluff_probability"] = max(0.2, params["bluff_probability"] - 0.01)
    
    def print_stats(self):
        """Imprime estatísticas de aprendizado"""
        print(f"\n{'='*60}")
        print(f"📊 ESTATÍSTICAS DE APRENDIZADO")
        print(f"{'='*60}")
        print(f"Total de partidas: {self.learning_data['total_games']}")
        print(f"Vitórias: {self.learning_data['total_wins']}")
        print(f"Derrotas: {self.learning_data['total_losses']}")
        print(f"Taxa de vitória: {self.get_win_rate()*100:.1f}%")
        print(f"Taxa recente (últimas 20): {self.get_recent_win_rate()*100:.1f}%")
        
        print(f"\n📈 Parâmetros de Estratégia:")
        for key, value in self.learning_data["strategy_params"].items():
            print(f"   {key}: {value:.2f}")
        
        print(f"\n🎯 Taxa de Sucesso por Ação:")
        for action, stats in self.learning_data["action_success_rates"].items():
            if stats["attempts"] > 0:
                rate = stats["success"] / stats["attempts"]
                print(f"   {action}: {rate*100:.1f}% ({stats['success']}/{stats['attempts']})")
        
        print(f"{'='*60}\n")

