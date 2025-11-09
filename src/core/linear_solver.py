import numpy as np
from typing import Tuple, Optional

class LinearSystemSolver:
    def __init__(self):
        """
        Attributs pour stocker la matrice A, le vecteur b et la solution x
        """
        self.A: Optional[np.ndarray] = None
        self.b: Optional[np.ndarray] = None
        self.solution: Optional[np.ndarray] = None
    
    def solve(self, A: np.ndarray, b: np.ndarray) -> Tuple[bool, Optional[np.ndarray], str]:
        """
        Résout un système linéaire AX = b.
        """
        try:
            # Valide les types d'entrée
            if not isinstance(A, np.ndarray) or not isinstance(b, np.ndarray):
                return False, None, "Les entrées doivent être des arrays NumPy"
            
            # Convertit en float pour la stabilité numérique
            A = A.astype(float)
            b = b.astype(float)
            
            # Valide les dimensions de la matrice A
            if A.ndim != 2:
                return False, None, "La matrice A doit être bidimensionnelle"
            
            n, m = A.shape
            if n != m:
                return False, None, f"La matrice A doit être carrée (reçu {n}x{m})"
            
            # Aplatit le vecteur b s'il est 2D
            if b.ndim == 2:
                b = b.flatten()
            
            # Valide les dimensions du vecteur b
            if len(b) != n:
                return False, None, f"Dimensions incompatibles : A est {n}x{n} mais b a {len(b)} éléments"
            
            # Vérifie si la matrice est singulière (pas de solution unique)
            det = np.linalg.det(A)
            if abs(det) < 1e-10:
                return False, None, f"Matrice singulière (déterminant ≈ 0) : système sans solution unique"
            
            # Résout le système linéaire
            x = np.linalg.solve(A, b)
            
            # Calcule le résidu pour vérifier la précision de la solution
            residual = np.linalg.norm(A @ x - b)
            
            # Stocke les résultats
            self.A = A
            self.b = b
            self.solution = x
            
            message = f"✅ Solution trouvée (résidu = {residual:.2e})"
            return True, x, message
            
        except np.linalg.LinAlgError as e:
            # Gère les erreurs spécifiques d'algèbre linéaire
            return False, None, f"❌ Erreur d'algèbre linéaire : {str(e)}"
        
        except Exception as e:
            # Gère toute autre erreur inattendue
            return False, None, f"❌ Erreur inattendue : {str(e)}"
    
    def get_matrix_info(self, A: np.ndarray) -> dict:
        """
        Calcule et retourne diverses propriétés d'une matrice donnée
        """
        try:
            det = np.linalg.det(A)
            cond = np.linalg.cond(A)
            rank = np.linalg.matrix_rank(A)
            
            return {
                'determinant': det,
                'conditionnement': cond,
                'rang': rank,
                'inversible': abs(det) > 1e-10 # Une matrice est inversible si son déterminant est non nul
            }
        except Exception as e:
            return {'error': str(e)}
    
    def format_solution(self, x: np.ndarray) -> str:
        """
        Formate le vecteur solution en une chaîne lisible
        """
        if x is None:
            return "Aucune solution"
        
        result = []
        for i, val in enumerate(x, start=1):
            result.append(f"x{i} = {val:.6f}")
        
        return "\n".join(result)

def parse_matrix_input(text: str, rows: int, cols: int) -> Tuple[bool, Optional[np.ndarray], str]:
    """
    Analyse une entrée texte en un tableau NumPy (matrice ou vecteur)
    """
    try:
        text = text.strip()
        if not text:
            return False, None, "Entrée vide"
        
        # Divise le texte en lignes et filtre les lignes vides
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Valide le nombre de lignes
        if len(lines) != rows:
            return False, None, f"Attendu {rows} lignes, reçu {len(lines)}"
        
        matrix_data = []
        for i, line in enumerate(lines, start=1):
            values = line.split()
            
            # Valide le nombre de colonnes
            if len(values) != cols:
                return False, None, f"Ligne {i} : attendu {cols} valeurs, reçu {len(values)}"
            
            try:
                # Convertit les valeurs en float
                row = [float(v) for v in values]
                matrix_data.append(row)
            except ValueError:
                return False, None, f"Ligne {i} : valeurs non numériques détectées"
        
        matrix = np.array(matrix_data)
        return True, matrix, "✅ Matrice parsée avec succès"
    
    except Exception as e:
        return False, None, f"Erreur de parsing : {str(e)}"

if __name__ == "__main__":
    # Exemple d'utilisation pour les tests
    solver = LinearSystemSolver()
    
    A = np.array([
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])
    b = np.array([8, -11, -3])
    
    print("=== Test de résolution ===")
    success, x, message = solver.solve(A, b)
    print(message)
    
    if success:
        print("\nSolution :")
        print(solver.format_solution(x))
        
        print("\nVérification (AX) :")
        print(A @ x)
        print("\nVecteur b :")
        print(b)
        
        print("\nInfos matrice :")
        info = solver.get_matrix_info(A)
        for key, val in info.items():
            print(f"{key}: {val}")
    
    print("\n=== Test de parsing ===")
    text_input = """2 1 -1
-3 -1 2
-2 1 2"""
    success, matrix, msg = parse_matrix_input(text_input, 3, 3)
    print(msg)
    if success:
        print(matrix)