import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from core.regression import LinearRegressionModel, load_csv
except ImportError:
    print("module regression manquant")


class LinearRegressionTab:
    def __init__(self, parent, status_callback):
        """
        Prépare l'onglet régression linéaire
        """
        self.parent = parent
        self.status_callback = status_callback
        self.model = LinearRegressionModel()
        self.X = None  # Les x (données d'netrée)
        self.y = None  # Les y (données de sortie)
        self.setup_ui()

    def setup_ui(self):
        """
        Crée l'interface de l'onglet
        """
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill='both', expand=True)

        # Colonne de gauche : données + boutons
        left_frame = ttk.Frame(main_container, padding="20")
        left_frame.pack(side='left', fill='both', expand=True)

        # Chargement
        load_frame = ttk.LabelFrame(left_frame, text="Données", padding="15")
        load_frame.pack(fill='x', pady=(0, 15))

        # Option 1 : CSV
        ttk.Label(load_frame, text="1) Fichier CSV (2 colonnes x, y)").pack(anchor='w', pady=5)
        btn_frame1 = ttk.Frame(load_frame)
        btn_frame1.pack(fill='x', pady=5)
        ttk.Button(btn_frame1, text="Parcourir", command=self.load_csv_file, style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame1, text="Petit exemple", command=self.load_example_csv).pack(side='left', padx=5)

        ttk.Separator(load_frame, orient='horizontal').pack(fill='x', pady=15)

        # Option 2 : À la main
        ttk.Label(load_frame, text="2) Taper les points (x y à chaque ligne)").pack(anchor='w', pady=5)
        self.manual_input_text = scrolledtext.ScrolledText(load_frame, width=30, height=6, font=('Courier', 9))
        self.manual_input_text.pack(fill='x', pady=5)
        self.manual_input_text.insert('1.0', "1 2.1\n2 4.2\n3 5.8\n4 8.1\n5 10.2")
        ttk.Button(load_frame, text="Go", command=self.load_manual_data).pack(anchor='w', pady=5)

        # Aperçu
        data_frame = ttk.LabelFrame(left_frame, text="👁️ Aperçu", padding="10")
        data_frame.pack(fill='x', pady=(0, 15))
        self.data_preview_text = scrolledtext.ScrolledText(data_frame, width=40, height=8, font=('Courier', 9), state='disabled')
        self.data_preview_text.pack(fill='x')

        # Boutons d'action
        action_frame = ttk.Frame(left_frame)
        action_frame.pack(fill='x', pady=(0, 15))
        ttk.Button(action_frame, text="Calculer", command=self.compute_regression, style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="Tout effacer", command=self.reset_data).pack(side='left', padx=5)

        # Résultats
        metrics_frame = ttk.LabelFrame(left_frame, text="Résultats", padding="10")
        metrics_frame.pack(fill='both', expand=True)
        self.metrics_text = scrolledtext.ScrolledText(metrics_frame, width=40, height=10, font=('Courier', 9), state='disabled')
        self.metrics_text.pack(fill='both', expand=True)

        # Colonne de droite : graph
        right_frame = ttk.Frame(main_container, padding="20")
        right_frame.pack(side='right', fill='both', expand=True)
        viz_frame = ttk.LabelFrame(right_frame, text="Graphique", padding="10")
        viz_frame.pack(fill='both', expand=True)
        self.canvas_frame = ttk.Frame(viz_frame)
        self.canvas_frame.pack(fill='both', expand=True)
        self.no_plot_label = ttk.Label(self.canvas_frame, text="Pas encore de graph\n\nCharge des données puis calcule", justify='center')
        self.no_plot_label.pack(expand=True)

    def load_csv_file(self):
        """
        Ouvre le choix de fichier et charge le CSV
        """
        filepath = filedialog.askopenfilename(
            title="Choisis un CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return

        success, X, y, message = load_csv(filepath)
        if not success:
            messagebox.showerror("Erreur", message)
            return

        self.X = X
        self.y = y
        self.update_data_preview()
        self.status_callback(message)

    def load_example_csv(self):
        """
        Mets un petit jeu d'essai
        """
        np.random.seed(42)
        self.X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.y = 2 * self.X + 1 + np.random.normal(0, 0.5, size=self.X.shape)
        self.update_data_preview()
        self.status_callback("Exemple prêt : 10 points (y ≈ 2x + 1)")

    def load_manual_data(self):
        """
        Récupère les points tapés
        """
        try:
            text = self.manual_input_text.get('1.0', 'end').strip()
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            if len(lines) < 2:
                messagebox.showwarning("Attention", "Il faut au moins 2 points")
                return

            X, y = [], []
            for i, line in enumerate(lines, start=1):
                parts = line.split()
                if len(parts) != 2:
                    messagebox.showerror("Erreur", f"Ligne {i} : faut mettre x y")
                    return
                try:
                    X.append(float(parts[0]))
                    y.append(float(parts[1]))
                except ValueError:
                    messagebox.showerror("Erreur", f"Ligne {i} : faut des nombres")
                    return

            self.X = np.array(X)
            self.y = np.array(y)
            self.update_data_preview()
            self.status_callback(f"{len(X)} points récupérés")
        except Exception as e:
            messagebox.showerror("Erreur", f"Problème :\n{str(e)}")

    def update_data_preview(self):
        """
        Affiche les données chargées
        """
        if self.X is None or self.y is None:
            return

        self.data_preview_text.config(state='normal')
        self.data_preview_text.delete('1.0', 'end')

        lines = []
        lines.append("x       | y")
        lines.append("-" * 20)
        n = len(self.X)
        max_display = 15
        for i in range(min(n, max_display)):
            lines.append(f"{self.X[i]:<7.2f} | {self.y[i]:<7.2f}")
        if n > max_display:
            lines.append(f"... ({n - max_display} de plus)")
        lines.append("-" * 20)
        lines.append(f"Total : {n} points")

        self.data_preview_text.insert('1.0', '\n'.join(lines))
        self.data_preview_text.config(state='disabled')

    def reset_data(self):
        """
        Remet tout à zéro
        """
        self.X = None
        self.y = None

        self.data_preview_text.config(state='normal')
        self.data_preview_text.delete('1.0', 'end')
        self.data_preview_text.config(state='disabled')

        self.metrics_text.config(state='normal')
        self.metrics_text.delete('1.0', 'end')
        self.metrics_text.config(state='disabled')

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        self.no_plot_label = ttk.Label(self.canvas_frame, text="Pas encore de graph\n\nCharge des données puis calcule", justify='center')
        self.no_plot_label.pack(expand=True)

        self.status_callback("On recommence à zéro")

    def compute_regression(self):
        """
        Lance le calcul
        """
        if self.X is None or self.y is None:
            messagebox.showwarning("Attention", "Données ?")
            return

        try:
            self.status_callback("Calcul en cours...")
            success, message = self.model.fit(self.X, self.y)

            if not success:
                messagebox.showerror("Erreur", message)
                return

            self.display_metrics()
            self.visualize_regression()
            r2 = self.model.metrics['r2']
            self.status_callback(f"Fait : {self.model.get_equation()} (R² = {r2:.4f})")
        except Exception as e:
            messagebox.showerror("Erreur", f"Souci :\n{str(e)}")

    def display_metrics(self):
        """
        Montre les chiffres
        """
        self.metrics_text.config(state='normal')
        self.metrics_text.delete('1.0', 'end')
        self.metrics_text.insert('1.0', self.model.format_metrics())
        self.metrics_text.config(state='disabled')

    def visualize_regression(self):
        """
        Dessine le nuage + droite
        """
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig = self.model.plot(title="Régression linéaire")
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig)
