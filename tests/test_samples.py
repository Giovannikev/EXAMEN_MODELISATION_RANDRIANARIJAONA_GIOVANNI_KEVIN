"""
test  manuels pr vrifier que les modules marchent bien.

lance ce fichier pr check que tous les calcules sont ok.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.linear_solver import LinearSystemSolver
from core.lp_solver import LinearProgrammingSolver
from core.regression import LinearRegressionModel


def test_linear_system():
    print("=" * 70)
    print("TEST 1 : RÉSO DE SYSTÈME LINÉAIRE (3×3)")
    print("=" * 70)
    
    solver = LinearSystemSolver()
    
    A = np.array([
        [2, 1, -1],
        [-3, -1, 2],
        [-2, 1, 2]
    ])
    b = np.array([8, -11, -3])
    
    print("\nMatrice A :")
    print(A)
    print("\nVecteur b :")
    print(b)
    
    success, x, message = solver.solve(A, b)
    
    print(f"\n{message}")
    
    if success:
        print("\nSOLUTION :")
        print(solver.format_solution(x))
        
        print("\nVÉRIF (AX) :")
        verification = A @ x
        print(verification)
        print("\nÉcart avec b :")
        print(np.abs(verification - b))
        
        if np.allclose(verification, b):
            print("\nTEST OK : la solution est bonne")
        else:
            print("\nTEST FAIL : la solution est nulle")
    else:
        print("\nTEST FAIL : problème de résolution")
    
    print()


def test_linear_programming():
    print("=" * 70)
    print("TEST 2 : PROG LINEAIRE")
    print("=" * 70)
    
    solver = LinearProgrammingSolver()
    
    objective = [3, 2]
    constraints = [
        {'coeffs': [2, 1], 'sense': '<=', 'rhs': 18},
        {'coeffs': [2, 3], 'sense': '<=', 'rhs': 42},
        {'coeffs': [3, 1], 'sense': '<=', 'rhs': 24}
    ]
    
    print("\nFonction objectif : Z = 3x₁ + 2x₂")
    print("\nContraintes :")
    for i, c in enumerate(constraints, start=1):
        print(f"  {i}. {c['coeffs'][0]}x₁ + {c['coeffs'][1]}x₂ {c['sense']} {c['rhs']}")
    print("  4. x₁, x₂ ≥ 0")
    
    success, solution, message = solver.solve(objective, constraints, sense="max")
    
    print(f"\n{message}")
    
    if success:
        print("\nSOLUTION :")
        print(solver.format_solution())
        
        expected = {'x1': 3, 'x2': 12}
        actual = solution
        
        x1_close = abs(actual['x1'] - expected['x1']) < 0.1
        x2_close = abs(actual['x2'] - expected['x2']) < 0.1
        
        if x1_close and x2_close:
            print("\nTEST OK : solution proche du attendu (x₁=3, x₂=12)")
        else:
            print(f"\nTEST PARTIEL : solution différente du attendu")
            print(f"   Attendu : x₁={expected['x1']}, x₂={expected['x2']}")
            print(f"   Obtenu  : x₁={actual['x1']:.2f}, x₂={actual['x2']:.2f}")
    else:
        print("\nTEST FAIL : erreur d'opti")
    
    print()


def test_linear_regression():
    print("=" * 70)
    print("TEST 3 : RÉGR LINEAIRE")
    print("=" * 70)
    
    model = LinearRegressionModel()
    
    np.random.seed(42)
    X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = 2 * X + 1 + np.random.normal(0, 0.3, size=X.shape)
    
    print("\nDonnées (10 points) :")
    print("x :", X)
    print("y :", y.round(2))
    
    success, message = model.fit(X, y)
    
    print(f"\n{message}")
    
    if success:
        print("\nRÉSULTATS :")
        print(f"Équation : {model.get_equation()}")
        print(f"Coef directeur (a) : {model.metrics['slope']:.4f}")
        print(f"Ordonnée à l'origine (b) : {model.metrics['intercept']:.4f}")
        print(f"R² : {model.metrics['r2']:.4f}")
        print(f"RMSE : {model.metrics['rmse']:.4f}")
        
        slope_close = abs(model.metrics['slope'] - 2.0) < 0.2
        r2_good = model.metrics['r2'] > 0.95
        
        if slope_close and r2_good:
            print("\nTEST OK : modèle proche de y = 2x + 1 avec bon R²")
        else:
            print("\nTEST PARTIEL : modèle passable mais y a un écart")
    else:
        print("\nTEST FAIL : erreur d'entrainement")
    
    print()


def main():
    print("\n")
    print("█" * 70)
    print("  SUITE DE TESTS - APP DE MODÉLISATION MATH")
    print("█" * 70)
    print()
    
    try:
        test_linear_system()
        test_linear_programming()
        test_linear_regression()
        
        print("=" * 70)
        print("TOUS LES TESTS SONT FINIS")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"\nERREUR PENDANT LES TESTS : {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()