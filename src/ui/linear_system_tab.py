import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from core.linear_solver import LinearSystemSolver, parse_matrix_input
except ImportError:
    print("linear_solver manquant")


class LinearSystemTab:
    
    def __init__(self, parent, status_callback):
        """
        Crée l'onglet « Systèmes linéaires »
        """
        self.parent = parent
        self.status_callback = status_callback
        self.solver = LinearSystemSolver()
        
        self.matrix_size = tk.IntVar(value=3)  # taille par défaut 3×3
        
        self.setup_ui()
    
    def setup_ui(self):
        """
        Construit l'interface : choix de la taille, zones de saisie, boutons et résultats
        """
        main_frame = ttk.Frame(self.parent, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Zone « Taille »
        config_frame = ttk.LabelFrame(main_frame, text="Taille", padding="15")
        config_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(config_frame, text="Taille de la matrice (n × n) :").grid(row=0, column=0, sticky='w', padx=5)
        
        size_frame = ttk.Frame(config_frame)
        size_frame.grid(row=0, column=1, sticky='w', padx=10)
        
        ttk.Radiobutton(size_frame, text="2×2", variable=self.matrix_size, value=2).pack(side='left', padx=5)
        ttk.Radiobutton(size_frame, text="3×3", variable=self.matrix_size, value=3).pack(side='left', padx=5)
        ttk.Radiobutton(size_frame, text="4×4", variable=self.matrix_size, value=4).pack(side='left', padx=5)
        
        ttk.Button(config_frame, text="Go", command=self.generate_fields, style='Action.TButton').grid(row=0, column=2, padx=10)
        
        # Zone « Saisie »
        input_frame = ttk.LabelFrame(main_frame, text="Matrice & vecteur", padding="15")
        input_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        matrices_frame = ttk.Frame(input_frame)
        matrices_frame.pack(fill='both', expand=True)
        
        # Matrice A
        a_frame = ttk.Frame(matrices_frame)
        a_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(a_frame, text="Matrice A", font=('Helvetica', 11, 'bold')).pack(anchor='w')
        ttk.Label(a_frame, text="Une ligne par ligne, espaces entre les nombres", font=('Helvetica', 9, 'italic')).pack(anchor='w', pady=(0, 5))
        
        self.matrix_a_text = scrolledtext.ScrolledText(a_frame, width=40, height=12, font=('Courier', 10))
        self.matrix_a_text.pack(fill='both', expand=True)
        
        # Vecteur b
        b_frame = ttk.Frame(matrices_frame)
        b_frame.pack(side='left', fill='both', expand=True)
        
        ttk.Label(b_frame, text="Vecteur b", font=('Helvetica', 11, 'bold')).pack(anchor='w')
        ttk.Label(b_frame, text="Une valeur par ligne", font=('Helvetica', 9, 'italic')).pack(anchor='w', pady=(0, 5))
        
        self.vector_b_text = scrolledtext.ScrolledText(b_frame, width=20, height=12, font=('Courier', 10))
        self.vector_b_text.pack(fill='both', expand=True)
        
        # Boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Button(action_frame, text="Résoudre", command=self.solve_system, style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="Reset", command=self.reset_fields).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Exemple 3×3", command=self.load_example).pack(side='left', padx=5)
        
        # Zone « Résultats »
        result_frame = ttk.LabelFrame(main_frame, text="Résultats", padding="15")
        result_frame.pack(fill='both', expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=80, height=10, font=('Courier', 10), state='disabled')
        self.result_text.pack(fill='both', expand=True)
        
        self.load_example()  # on met un exemple dès le départ
    
    def generate_fields(self):
        """
        Efface tout et affiche un petit message pour dire qu'on est prêt
        """
        n = self.matrix_size.get()
        self.reset_fields()
        self.status_callback(f"Prêt pour une matrice {n}×{n}")
    
    def reset_fields(self):
        """
        Remet les zones à zéro
        """
        self.matrix_a_text.delete('1.0', 'end')
        self.vector_b_text.delete('1.0', 'end')
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', 'end')
        self.result_text.config(state='disabled')
        self.status_callback("Zones vidées")
    
    def load_example(self):
        """
        Charge un petit exemple 3×3
        """
        self.matrix_size.set(3)
        
        example_a = """2 1 -1
-3 -1 2
-2 1 2"""
        
        example_b = """8
-11
-3"""
        
        self.matrix_a_text.delete('1.0', 'end')
        self.matrix_a_text.insert('1.0', example_a)
        
        self.vector_b_text.delete('1.0', 'end')
        self.vector_b_text.insert('1.0', example_b)
        
        self.status_callback("Exemple prêt : solution (2, 3, -1)")
    
    def solve_system(self):
        """
        Lance le calcul et affiche ce qu'il se passe
        """
        try:
            n = self.matrix_size.get()
            
            a_text = self.matrix_a_text.get('1.0', 'end')
            success_a, A, msg_a = parse_matrix_input(a_text, n, n)
            
            if not success_a:
                messagebox.showerror("Oups", f"Matrice A pas claire :\n{msg_a}")
                return
            
            b_text = self.vector_b_text.get('1.0', 'end')
            success_b, b, msg_b = parse_matrix_input(b_text, n, 1)
            
            if not success_b:
                messagebox.showerror("Oups", f"Vecteur b pas clair :\n{msg_b}")
                return
            
            b = b.flatten()
            
            self.status_callback("Je calcule…")
            success, solution, message = self.solver.solve(A, b)
            
            if not success:
                messagebox.showerror("Pas possible", message)
                self.status_callback("Calcul planté")
                return
            
            self.display_results(A, b, solution, message)
            self.status_callback("Ça marche !")
            
        except Exception as e:
            messagebox.showerror("Zut", f"Problème :\n{str(e)}")
            self.status_callback("Ça a foiré")
    
    def display_results(self, A, b, solution, message):
        """
        Affiche la solution et quelques infos rapides.
        """
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', 'end')
        
        output = []
        output.append("=" * 50)
        output.append("Résolution de A x = b")
        output.append("=" * 50)
        output.append("")
        
        matrix_info = self.solver.get_matrix_info(A)
        output.append("Détails sur A :")
        output.append(f"  Déterminant : {matrix_info.get('determinant', 'N/A'):.6f}")
        output.append(f"  Conditionnement : {matrix_info.get('conditionnement', 'N/A'):.6f}")
        output.append(f"  Rang : {matrix_info.get('rang', 'N/A')}")
        output.append(f"  Inversible : {'Oui' if matrix_info.get('inversible') else 'Non'}")
        output.append("")
        
        output.append("Solution :")
        output.append(self.solver.format_solution(solution))
        output.append("")
        
        verification = A @ solution
        output.append("Vérification A x :")
        for i, val in enumerate(verification, start=1):
            output.append(f"  Ligne {i} : {val:.6f} ≈ {b[i-1]:.6f}")
        
        output.append("")
        output.append(message)
        output.append("=" * 50)
        
        self.result_text.insert('1.0', '\n'.join(output))
        self.result_text.config(state='disabled')