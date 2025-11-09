import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from ui.linear_system_tab import LinearSystemTab
    from ui.linear_programming_tab import LinearProgrammingTab
    from ui.linear_regression_tab import LinearRegressionTab
except ImportError:
    from linear_system_tab import LinearSystemTab
    from linear_programming_tab import LinearProgrammingTab
    from linear_regression_tab import LinearRegressionTab


class MathModelingApp:
    
    def __init__(self, root):
        """
        Initialise l'interface de modélisation mathématique
        """
        self.root = root
        self.root.title("Outil de Modélisation Mathématique")
        self.root.geometry("1200x800")
        
        self.configure_styles()
        self.build_menu()
        self.build_statusbar()
        self.build_tabs()
        self.center_window()
    
    def configure_styles(self):
        """
        Paramètre l'apparence visuelle via ttk.Style
        """
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Helvetica', 10, 'bold'))
        
        style.configure('Action.TButton', font=('Helvetica', 11, 'bold'), padding=10)
        
        style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'))
        style.configure('Subtitle.TLabel', font=('Helvetica', 10))
    
    def build_menu(self):
        """
        Construit le menu principal avec Fichier et Aide
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Quitter", command=self.exit_app, accelerator="Ctrl+Q")
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.display_about)
        help_menu.add_command(label="Guide rapide", command=self.display_guide)
        
        self.root.bind('<Control-q>', lambda e: self.exit_app())
    
    def build_tabs(self):
        """
        Ajoute les trois modules principaux dans des onglets séparés
        """
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Onglet Systèmes linéaires
        self.linear_system_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.linear_system_frame, text="Systèmes linéaires")
        self.linear_system_tab = LinearSystemTab(self.linear_system_frame, self.refresh_status)
        
        # Onglet Programmation linéaire
        self.lp_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.lp_frame, text="Programmation linéaire")
        self.lp_tab = LinearProgrammingTab(self.lp_frame, self.refresh_status)
        
        # Onglet Régression linéaire
        self.regression_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.regression_frame, text="Régression linéaire")
        self.regression_tab = LinearRegressionTab(self.regression_frame, self.refresh_status)
    
    def build_statusbar(self):
        """
        Barre d'état en bas de la fenêtre
        """
        self.statusbar = ttk.Label(
            self.root,
            text="Prêt | Choisissez un onglet ci-dessus",
            relief=tk.SUNKEN,
            anchor='w',
            padding=(5, 2)
        )
        self.statusbar.pack(side='bottom', fill='x')
    
    def refresh_status(self, message: str):
        """
        Actualise le libellé de la barre d'état
        """
        self.statusbar.config(text=message)
    
    def center_window(self):
        """
        Centre la fenêtre au milieu de l'écran
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def display_about(self):
        """
        Fenêtre À propos
        """
        about_text = """
Outil de Modélisation Mathématique
Version 1.0

Projet académique L2 IDEV – RSI
Modélisation mathématique

Fonctionnalités :
• Résolution de systèmes linéaires (AX = b)
• Optimisation en programmation linéaire
• Ajustement par régression linéaire

Stack : Python, NumPy, Matplotlib, PuLP, scikit-learn, Tkinter
        """
        messagebox.showinfo("À propos", about_text.strip())
    
    def display_guide(self):
        """
        Petit guide utilisateur
        """
        doc_text = """
Petit guide

1. SYSTÈMES LINÉAIRES
   - Indiquez la dimension (ex : 3×3)
   - Remplissez la matrice A et le vecteur b
   - Cliquez sur « Résoudre »

2. PROGRAMMATION LINÉAIRE
   - Sélectionnez Maximiser ou Minimiser
   - Saisissez la fonction objectif (ex : 3 2 pour 3x + 2y)
   - Ajoutez les contraintes une à une
   - Lancez « Résoudre et Visualiser »

3. RÉGRESSION LINÉAIRE
   - Importez un CSV (colonnes x, y)
   - Ou entrez les points à la main
   - Cliquez sur « Calculer la régression »
   - Le graphique et les indicateurs apparaissent

Pour plus de détails, lisez le README.md
        """
        messagebox.showinfo("Guide rapide", doc_text.strip())
    
    def exit_app(self):
        """
        Confirmation de fermeture
        """
        if messagebox.askokcancel("Quitter", "Fermer l'application ?"):
            self.root.quit()


def main():
    """
    Lance l'outil de modélisation mathématique
    """
    root = tk.Tk()
    app = MathModelingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()