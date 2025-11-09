# Documentation d'installation et de lancement

Cette documentation vous guidera à travers les étapes nécessaires pour installer et lancer le projet.

## 1. Installation

Suivez les étapes ci-dessous pour configurer votre environnement de développement.

### 1.1. Cloner le dépôt

Ouvrez votre terminal ou invite de commande et exécutez la commande suivante pour cloner le dépôt Git:

```bash
git clone https://github.com/Giovannikev/EXAMEN_MODELISATION_RANDRIANARIJAONA_GIOVANNI_KEVIN.git
cd EXAMEN_MODELISATION_RANDRIANARIJAONA_GIOVANNI_KEVIN
```

### 1.2. Créer et activer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour gérer les dépendances du projet.

```bash
python -m venv .venv
```

- **Sur Windows:**

  ```bash
  .\.venv\Scripts\activate
  ```

- **Sur macOS/Linux:**

  ```bash
  source ./.venv/bin/activate
  ```

### 1.3. Installer les dépendances

Une fois l'environnement virtuel activé, installez les dépendances Python requises en utilisant `pip`:

```bash
pip install -r requirements.txt
```

## 2. Lancement du projet

Pour lancer l'application, assurez-vous que votre environnement virtuel est activé et exécutez le script principal:

```bash
python src/main.py
```

### 2.1. Exécuter les tests

Pour exécuter les tests du projet, assurez-vous que votre environnement virtuel est activé et exécutez la commande suivante:

```bash
python tests/test_samples.py
```