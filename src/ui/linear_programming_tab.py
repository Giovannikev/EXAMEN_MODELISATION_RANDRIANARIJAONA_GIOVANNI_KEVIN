import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from core.lp_solver import LinearProgrammingSolver
except ImportError:
    print("lp_solver manquant")


class LinearProgrammingTab:
    def __init__(self, parent, status_callback):
        """
        Initialise l'onglet de programmation linéaire
        """
        self.parent = parent
        self.status_callback = status_callback
        self.solver = LinearProgrammingSolver()
        self.sense_var = tk.StringVar(value="max")  # Variable pour le sens de l'optimisation (maximiser/minimiser)
        self.constraints_list = []  # Liste pour stocker les contraintes ajoutées
        self.setup_ui()

    def setup_ui(self):
        """
        Configure l'interface utilisateur de l'onglet de programmation linéaire
        """
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill='both', expand=True)

        # Cadre gauche pour la saisie et les résultats
        left_frame = ttk.Frame(main_container, padding="20")
        left_frame.pack(side='left', fill='both', expand=True)

        # Section Fonction objectif
        obj_frame = ttk.LabelFrame(left_frame, text="Fonction objectif", padding="15")
        obj_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(obj_frame, text="Type :").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Radiobutton(obj_frame, text="Maximiser", variable=self.sense_var, value="max").grid(row=0, column=1, sticky='w', padx=5)
        ttk.Radiobutton(obj_frame, text="Minimiser", variable=self.sense_var, value="min").grid(row=0, column=2, sticky='w', padx=5)
        ttk.Label(obj_frame, text="Coefficients (ex: 3 2 pour 3x₁ + 2x₂) :").grid(row=1, column=0, columnspan=3, sticky='w', padx=5, pady=(10, 0))
        self.objective_entry = ttk.Entry(obj_frame, width=40, font=('Courier', 10))
        self.objective_entry.grid(row=2, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        self.objective_entry.insert(0, "3 2") # Valeur par défaut

        # Section Contraintes
        constraints_frame = ttk.LabelFrame(left_frame, text="Contraintes", padding="15")
        constraints_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Cadre pour ajouter une nouvelle contrainte
        add_frame = ttk.Frame(constraints_frame)
        add_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(add_frame, text="Coefficients :").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.constraint_coeffs_entry = ttk.Entry(add_frame, width=20, font=('Courier', 10))
        self.constraint_coeffs_entry.grid(row=0, column=1, padx=5)
        self.constraint_coeffs_entry.insert(0, "2 1") # Valeur par défaut
        self.constraint_sense_var = tk.StringVar(value="<=")
        ttk.Combobox(add_frame, textvariable=self.constraint_sense_var, values=["<=", ">=", "=="], width=5, state='readonly').grid(row=0, column=2, padx=5)
        ttk.Label(add_frame, text="RHS :").grid(row=0, column=3, sticky='w', padx=5)
        self.constraint_rhs_entry = ttk.Entry(add_frame, width=10, font=('Courier', 10))
        self.constraint_rhs_entry.grid(row=0, column=4, padx=5)
        self.constraint_rhs_entry.insert(0, "18") # Valeur par défaut
        ttk.Button(add_frame, text="Ajouter", command=self.add_constraint).grid(row=0, column=5, padx=10)

        ttk.Label(constraints_frame, text="Contraintes ajoutées :", font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(10, 5))

        # Liste des contraintes ajoutées
        list_frame = ttk.Frame(constraints_frame)
        list_frame.pack(fill='both', expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        self.constraints_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Courier', 9), height=8)
        self.constraints_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.constraints_listbox.yview)

        # Boutons pour gérer les contraintes
        btn_frame = ttk.Frame(constraints_frame)
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="Supprimer sélection", command=self.remove_constraint).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Tout effacer", command=self.clear_constraints).pack(side='left', padx=5)

        # Cadre d'actions (résoudre, charger exemple)
        action_frame = ttk.Frame(left_frame)
        action_frame.pack(fill='x', pady=(0, 15))
        ttk.Button(action_frame, text="Résoudre et Visualiser", command=self.solve_and_visualize, style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="Charger exemple", command=self.load_example).pack(side='left', padx=5)

        # Cadre des résultats
        result_frame = ttk.LabelFrame(left_frame, text="Résultats", padding="10")
        result_frame.pack(fill='both', expand=True)
        self.result_text = scrolledtext.ScrolledText(result_frame, width=60, height=8, font=('Courier', 9), state='disabled')
        self.result_text.pack(fill='both', expand=True)

        # Cadre droit pour la visualisation
        right_frame = ttk.Frame(main_container, padding="20")
        right_frame.pack(side='right', fill='both', expand=True)
        viz_frame = ttk.LabelFrame(right_frame, text="Visualisation (2D uniquement)", padding="10")
        viz_frame.pack(fill='both', expand=True)
        self.canvas_frame = ttk.Frame(viz_frame) # Cadre pour le graphique Matplotlib
        self.canvas_frame.pack(fill='both', expand=True)
        self.no_plot_label = ttk.Label(self.canvas_frame, text="Pas de graphique\n\nRésous un pb à 2 vars pour voir", justify='center')
        self.no_plot_label.pack(expand=True)

        self.load_example() # Charge un exemple au démarrage

    def add_constraint(self):
        """
        Ajoute une nouvelle contrainte à la liste des contraintes du problème
        """
        try:
            coeffs_text = self.constraint_coeffs_entry.get().strip()
            coeffs = [float(x) for x in coeffs_text.split()] # Convertit les coefficients en flottants
            sense = self.constraint_sense_var.get()
            rhs = float(self.constraint_rhs_entry.get())

            constraint = {
                'coeffs': coeffs,
                'sense': sense,
                'rhs': rhs
            }
            self.constraints_list.append(constraint)
            display_text = f"{' '.join([f'{c:.1f}' for c in coeffs])} {sense} {rhs:.1f}"
            self.constraints_listbox.insert('end', display_text)
            self.status_callback(f"Contrainte ajoutée : {display_text}")
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides. Vérifiez les coefficients et RHS.")

    def remove_constraint(self):
        """
        Supprime la contrainte sélectionnée de la liste.
        """
        selection = self.constraints_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Aucune contrainte sélectionnée")
            return
        index = selection[0]
        self.constraints_listbox.delete(index)
        del self.constraints_list[index]
        self.status_callback("Contrainte supprimée")

    def clear_constraints(self):
        """
        Efface toutes les contraintes de la liste et de l'affichage.
        """
        self.constraints_listbox.delete(0, 'end')
        self.constraints_list.clear()
        self.status_callback("Toutes les contraintes ont été effacées")

    def load_example(self):
        """
        Charge un exemple prédéfini de problème de programmation linéaire
        """
        self.objective_entry.delete(0, 'end')
        self.objective_entry.insert(0, "3 2")
        self.sense_var.set("max")
        self.clear_constraints()
        example_constraints = [
            {'coeffs': [2, 1], 'sense': '<=', 'rhs': 18},
            {'coeffs': [2, 3], 'sense': '<=', 'rhs': 42},
            {'coeffs': [3, 1], 'sense': '<=', 'rhs': 24}
        ]
        for c in example_constraints:
            self.constraints_list.append(c)
            display_text = f"{' '.join([f'{coef:.1f}' for coef in c['coeffs']])} {c['sense']} {c['rhs']:.1f}"
            self.constraints_listbox.insert('end', display_text)
        self.status_callback("Exemple chargé : Max Z = 3x₁ + 2x₂ avec 3 contraintes")

    def solve_and_visualize(self):
        """
        Résout le problème de programmation linéaire et visualise la solution si possible
        """
        try:
            obj_text = self.objective_entry.get().strip()
            objective_coeffs = [float(x) for x in obj_text.split()] # Coefficients de la fonction objectif

            if not self.constraints_list:
                messagebox.showwarning("Attention", "Aucune contrainte définie")
                return

            sense = self.sense_var.get()
            self.status_callback("Résolution en cours...")

            # Appelle le solveur de programmation linéaire
            success, solution, message = self.solver.solve(objective_coeffs, self.constraints_list, sense)

            if not success:
                messagebox.showerror("Échec", message)
                self.status_callback("Échec de la résolution")
                return

            self.display_results(solution, message)

            # Visualisation 2D uniquement si 2 variables
            if len(objective_coeffs) == 2:
                self.visualize_solution(objective_coeffs, sense)
            else:
                messagebox.showinfo("Info", "Visualisation 2D non disponible pour plus de 2 variables")

            self.status_callback(f"Solution optimale trouvée : Z = {self.solver.objective_value:.4f}")

        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeurs invalides :\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur inattendue :\n{str(e)}")

    def display_results(self, solution, message):
        """
        Affiche les résultats de la résolution dans la zone de texte des résultats
        """
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', 'end')
        output = []
        output.append("=" * 50)
        output.append("RÉSULTATS DE L'OPTIMISATION")
        output.append("=" * 50)
        output.append("")
        output.append(self.solver.format_solution())
        output.append("")
        output.append(f"Statut : {message}")
        output.append("=" * 50)
        self.result_text.insert('1.0', '\n'.join(output))
        self.result_text.config(state='disabled')

    def visualize_solution(self, objective_coeffs, sense):
        """
        Affiche la visualisation 2D du problème de programmation linéaire.
        Efface le graphique précédent et en génère un nouveau avec la solution
        """
        for widget in self.canvas_frame.winfo_children():
            widget.destroy() # Supprime les widgets précédents du cadre de visualisation

        fig = self.solver.visualize_2d(objective_coeffs, self.constraints_list, sense)
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig) # Ferme la figure Matplotlib pour libérer de la mémoire