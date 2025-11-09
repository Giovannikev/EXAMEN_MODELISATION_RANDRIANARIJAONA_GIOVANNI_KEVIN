import pulp
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional


class LinearProgrammingSolver:
    def __init__(self):
        """
        Initialise le LinearProgrammingSolver.
        Attributs pour stocker le problème LP, les variables, la solution et la valeur de la fonction objectif
        """
        self.problem: Optional[pulp.LpProblem] = None
        self.variables: Dict[str, pulp.LpVariable] = {}
        self.solution: Dict[str, float] = {}
        self.objective_value: Optional[float] = None
    
    def solve(
        self,
        objective_coeffs: List[float],
        constraints: List[Dict],
        sense: str = "max",
        var_names: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[Dict], str]:
        """
        Résout un problème de programmation linéaire
        """
        try:
            n_vars = len(objective_coeffs)
            
            # Valider les dimensions des contraintes
            for i, c in enumerate(constraints):
                if len(c['coeffs']) != n_vars:
                    return False, None, f"Contrainte {i+1} : nombre de coefficients incorrect"
                if c['sense'] not in ['<=', '>=', '==']:
                    return False, None, f"Contrainte {i+1} : opérateur invalide '{c['sense']}'"
            
            # Créer le problème LP
            prob_name = f"LP_{sense.upper()}"
            sense_pulp = pulp.LpMaximize if sense.lower() == "max" else pulp.LpMinimize
            self.problem = pulp.LpProblem(prob_name, sense_pulp)
            
            # Définir les variables
            if var_names is None:
                var_names = [f"x{i+1}" for i in range(n_vars)]
            
            self.variables = {
                name: pulp.LpVariable(name, lowBound=0) # En supposant des variables non négatives
                for name in var_names
            }
            
            var_list = list(self.variables.values())
            
            # Définir la fonction objectif
            self.problem += pulp.lpSum([
                c * var for c, var in zip(objective_coeffs, var_list)
            ]), "Objective"
            
            # Ajouter les contraintes
            for i, constraint in enumerate(constraints):
                coeffs = constraint['coeffs']
                sense_str = constraint['sense']
                rhs = constraint['rhs']
                
                lhs = pulp.lpSum([c * var for c, var in zip(coeffs, var_list)])
                
                if sense_str == '<=':
                    self.problem += lhs <= rhs, f"Constraint_{i+1}"
                elif sense_str == '>=':
                    self.problem += lhs >= rhs, f"Constraint_{i+1}"
                elif sense_str == '==':
                    self.problem += lhs == rhs, f"Constraint_{i+1}"
            
            # Résoudre le problème
            self.problem.solve(pulp.PULP_CBC_CMD(msg=0)) # msg=0 supprime la sortie du solveur
            
            # Obtenir le statut de la solution
            status = pulp.LpStatus[self.problem.status]
            
            if status != "Optimal":
                return False, None, f"❌ Pas de solution optimale (statut : {status})"
            
            # Stocker la solution
            self.solution = {
                name: var.varValue
                for name, var in self.variables.items()
            }
            self.objective_value = pulp.value(self.problem.objective)
            
            message = f"✅ Solution optimale trouvée (Z = {self.objective_value:.4f})"
            return True, self.solution, message
        
        except Exception as e:
            return False, None, f"❌ Erreur : {str(e)}"
    
    def format_solution(self) -> str:
        """
        Formate la solution optimale trouvée en une chaîne lisible par l'homme
        """
        if not self.solution:
            return "Aucune solution"
        
        lines = []
        for name, value in self.solution.items():
            lines.append(f"{name} = {value:.6f}")
        
        if self.objective_value is not None:
            lines.append(f"\nValeur optimale Z = {self.objective_value:.6f}")
        
        return "\n".join(lines)
    
    def visualize_2d(
        self,
        objective_coeffs: List[float],
        constraints: List[Dict],
        sense: str = "max"
    ) -> plt.Figure:
        """
        Visualise un problème de programmation linéaire 2D
        """
        if len(objective_coeffs) != 2:
            raise ValueError("La visualisation 2D nécessite exactement 2 variables")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Définir une plage de valeurs pour l'axe des x
        x_vals = np.linspace(0, 20, 400)
        
        # Tracer chaque contrainte
        for i, c in enumerate(constraints):
            a, b = c['coeffs'][:2]
            rhs = c['rhs']
            sense_str = c['sense']
            
            if b != 0:
                y_vals = (rhs - a * x_vals) / b
                
                label = f"{a:.1f}x₁ + {b:.1f}x₂ {sense_str} {rhs:.1f}"
                ax.plot(x_vals, y_vals, label=label, linewidth=2)
                
                # Ombrer la région réalisable pour les inégalités
                if sense_str == '<=':
                    ax.fill_between(x_vals, 0, y_vals, alpha=0.1)
                elif sense_str == '>=':
                    ax.fill_between(x_vals, y_vals, 20, alpha=0.1) # En supposant une borne supérieure pour y
        
        # Ajouter des axes pour les contraintes de non-négativité
        ax.axhline(y=0, color='black', linewidth=0.8)
        ax.axvline(x=0, color='black', linewidth=0.8)
        
        # Tracer la solution optimale si disponible
        if self.solution and len(self.solution) == 2:
            vars_list = list(self.solution.values())
            x_opt, y_opt = vars_list[0], vars_list[1]
            ax.plot(x_opt, y_opt, 'ro', markersize=12, label=f'Optimal ({x_opt:.2f}, {y_opt:.2f})', zorder=5)
            ax.annotate(
                f'Z = {self.objective_value:.2f}',
                xy=(x_opt, y_opt),
                xytext=(10, 10),
                textcoords='offset points',
                fontsize=12,
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7)
            )
        
        # Définir les limites et étiquettes du graphique
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)
        ax.set_xlabel('x₁', fontsize=12)
        ax.set_ylabel('x₂', fontsize=12)
        ax.set_title(f'Région réalisable - {"Maximisation" if sense == "max" else "Minimisation"}', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


if __name__ == "__main__":
    # Exemple d'utilisation pour des tests
    solver = LinearProgrammingSolver()
    objective = [3, 2]
    constraints = [
        {'coeffs': [2, 1], 'sense': '<=', 'rhs': 18},
        {'coeffs': [2, 3], 'sense': '<=', 'rhs': 42},
        {'coeffs': [3, 1], 'sense': '<=', 'rhs': 24}
    ]
    
    print("=== Résolution du problème LP ===")
    success, solution, message = solver.solve(objective, constraints, sense="max")
    print(message)
    
    if success:
        print("\nSolution :")
        print(solver.format_solution())
        
        fig = solver.visualize_2d(objective, constraints, sense="max")
        plt.savefig('lp_solution.png', dpi=150, bbox_inches='tight')
        print("\n📊 Graphique sauvegardé : lp_solution.png")
        plt.show()