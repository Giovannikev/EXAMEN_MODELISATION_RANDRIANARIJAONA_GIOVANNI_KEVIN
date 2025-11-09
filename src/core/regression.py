import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from typing import Tuple, Optional, Dict
import csv


class LinearRegressionModel:
    def __init__(self):
        """
        Initialise le modèle de régression linéaire
        """
        self.model: LinearRegression = LinearRegression()
        self.X: Optional[np.ndarray] = None
        self.y: Optional[np.ndarray] = None
        self.is_fitted: bool = False
        self.metrics: Dict[str, float] = {}
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> Tuple[bool, str]:
        """
        Ajuste le modèle de régression linéaire aux données fournies
        """
        try:
            X = np.array(X).astype(float)
            y = np.array(y).astype(float)
            
            # Remodeler X si c'est un tableau 1D (une seule caractéristique)
            if X.ndim == 1:
                X = X.reshape(-1, 1)
            
            # Valider les dimensions
            if len(X) != len(y):
                return False, f"Dimensions incompatibles : X a {len(X)} éléments, y en a {len(y)}"
            if len(X) < 2:
                return False, "Au moins 2 points sont nécessaires pour la régression"
            
            self.X = X
            self.y = y
            self.model.fit(X, y)
            self.is_fitted = True
            
            # Calculer les métriques
            y_pred = self.model.predict(X)
            self.metrics = {
                'slope': self.model.coef_[0] if self.model.coef_.size > 0 else 0.0,
                'intercept': self.model.intercept_,
                'r2': r2_score(y, y_pred),
                'rmse': np.sqrt(mean_squared_error(y, y_pred)),
                'n_points': len(X)
            }
            
            return True, "✅ Modèle entraîné avec succès"
        except Exception as e:
            return False, f"❌ Erreur d'entraînement : {str(e)}"
    
    def predict(self, X_new: np.ndarray) -> Optional[np.ndarray]:
        """
        Effectue des prédictions à l'aide du modèle de régression linéaire ajusté
        """
        if not self.is_fitted:
            return None
        
        # Remodeler X_new si c'est un tableau 1D
        X_new = np.array(X_new).reshape(-1, 1)
        return self.model.predict(X_new)
    
    def get_equation(self) -> str:
        """
        Retourne l'équation de régression linéaire sous forme de chaîne de caractères
        """
        if not self.is_fitted:
            return "Modèle non entraîné"
        
        a = self.metrics['slope']
        b = self.metrics['intercept']
        sign = '+' if b >= 0 else '-'
        return f"y = {a:.4f}x {sign} {abs(b):.4f}"
    
    def format_metrics(self) -> str:
        """
        Formate les métriques de performance du modèle en une chaîne de caractères lisible par l'homme
        """
        if not self.is_fitted:
            return "Aucune métrique disponible"
        
        lines = [
            "📊 Métriques du modèle",
            "=" * 40,
            f"Équation : {self.get_equation()}",
            f"Coefficient directeur (a) : {self.metrics['slope']:.6f}",
            f"Ordonnée à l'origine (b) : {self.metrics['intercept']:.6f}",
            f"R² (coefficient de détermination) : {self.metrics['r2']:.6f}",
            f"RMSE (erreur quadratique moyenne) : {self.metrics['rmse']:.6f}",
            f"Nombre de points : {self.metrics['n_points']}"
        ]
        
        r2 = self.metrics['r2']
        if r2 > 0.9:
            lines.append("\n✅ Excellent ajustement (R² > 0.9)")
        elif r2 > 0.7:
            lines.append("\n⚠️ Bon ajustement (0.7 < R² < 0.9)")
        else:
            lines.append("\n❌ Ajustement moyen (R² < 0.7)")
        
        return "\n".join(lines)
    
    def plot(self, title: str = "Régression linéaire") -> plt.Figure:
        """
        Génère un graphique Matplotlib des données et de la ligne de régression ajustée
        """
        if not self.is_fitted:
            raise ValueError("Le modèle doit être entraîné avant de générer un graphique")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Tracer les points de données originaux
        ax.scatter(self.X, self.y, color='blue', s=100, alpha=0.6, edgecolors='black', label='Données')
        
        # Tracer la ligne de régression
        X_line = np.linspace(self.X.min(), self.X.max(), 100).reshape(-1, 1)
        y_line = self.model.predict(X_line)
        ax.plot(X_line, y_line, color='red', linewidth=2.5, label=f'Régression : {self.get_equation()}')
        
        # Tracer les résidus (lignes verticales des points de données à la ligne de régression)
        y_pred = self.model.predict(self.X)
        for i in range(len(self.X)):
            ax.plot([self.X[i], self.X[i]], [self.y[i], y_pred[i]], 'g--', alpha=0.3, linewidth=1)
        
        # Définir les étiquettes, le titre, la légende et la grille
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Ajouter R² et RMSE au graphique
        textstr = f"R² = {self.metrics['r2']:.4f}\nRMSE = {self.metrics['rmse']:.4f}"
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        return fig

def load_csv(filepath: str) -> Tuple[bool, Optional[np.ndarray], Optional[np.ndarray], str]:
    """
    Charge les données X et y à partir d'un fichier CSV
    """
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if len(rows) < 2:
            return False, None, None, "Le fichier doit contenir au moins 2 lignes de données"
        
        # Déterminer s'il y a un en-tête
        has_header = False
        try:
            float(rows[0][0])
        except ValueError:
            has_header = True
        
        data_rows = rows[1:] if has_header else rows
        
        X, y = [], []
        for i, row in enumerate(data_rows, start=1):
            if len(row) < 2:
                return False, None, None, f"Ligne {i} : moins de 2 colonnes"
            try:
                X.append(float(row[0]))
                y.append(float(row[1]))
            except ValueError:
                return False, None, None, f"Ligne {i} : valeurs non numériques"
        
        X = np.array(X)
        y = np.array(y)
        
        return True, X, y, f"✅ {len(X)} points chargés depuis {filepath}"
    except FileNotFoundError:
        return False, None, None, f"❌ Fichier introuvable : {filepath}"
    except Exception as e:
        return False, None, None, f"❌ Erreur de lecture : {str(e)}"

def save_csv(filepath: str, X: np.ndarray, y: np.ndarray) -> Tuple[bool, str]:
    """
    Sauvegarde les données X et y dans un fichier CSV avec un en-tête
    """
    try:
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y']) # Écrire l'en-tête
            for x_val, y_val in zip(X, y):
                writer.writerow([x_val, y_val])
        return True, f"✅ Données sauvegardées dans {filepath}"
    except Exception as e:
        return False, f"❌ Erreur d'écriture : {str(e)}"


if __name__ == "__main__":
    # Example usage for testing purposes
    np.random.seed(42)
    X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = 2 * X + 1 + np.random.normal(0, 0.5, size=X.shape)
    
    print("=== Test du modèle de régression ===")
    model = LinearRegressionModel()
    success, message = model.fit(X, y)
    print(message)
    
    if success:
        print("\n" + model.format_metrics())
        fig = model.plot(title="Régression linéaire - Données synthétiques")
        plt.savefig('regression_test.png', dpi=150, bbox_inches='tight')
        print("\n📊 Graphique sauvegardé : regression_test.png")
        
        X_new = np.array([11, 12, 13])
        y_pred = model.predict(X_new)
        print(f"\nPrédictions pour x = {X_new} :")
        print(f"y = {y_pred}")
        
        plt.show()