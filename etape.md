# 📚 Projet Django — Gestion de bibliothèque personnelle

Ce projet a pour but de créer une application backend en **Django** pour gérer une bibliothèque personnelle. Il inclura la gestion des livres, des listes de lecture (lu, à lire, favoris), des commentaires et des notes.

## 🧠 Objectif pédagogique

- Maîtriser le backend avec **Python** et **Django**
- Créer une **base de données relationnelle complexe** avec PostgreSQL
- Utiliser les **migrations** pour gérer le schéma de la BDD
- Remplir la base de données avec des **fixtures**
- Écrire des **tests unitaires** réguliers
- Tester les **routes API** avec Insomnia

---

## 🛠️ Étape 1 — Création du projet Django

### 1.1 — Créer un environnement de développement

```bash
# Créer un dossier pour le projet
mkdir django-biblio
cd django-biblio

# Créer un environnement virtuel Python
python -m venv env

# Activer l'environnement
# Sur Linux / macOS :
source env/bin/activate
# Sur Windows :
source env/Scripts/activate
```

### 1.2 — Installer les dépendances

```bash
pip install django
```

Permet de vérifier si l'installation c'est correctement effectué
```bash
python -m django --version
```

### 1.3 — Créer le projet Django

```bash
django-admin startproject biblio_backend .
```

### 1.4 — Arborescence du projet

django-biblio/  
├── env/                  # Environnement virtuel  
├── manage.py             # Script de gestion du projet  
├── biblio_backend/       # Dossier de configuration Django  
│   ├── __init__.py  
│   ├── settings.py       # Configuration principale  
│   ├── urls.py           # Routes principales  
│   ├── wsgi.py  
│   └── asgi.py  

### 1.5 — Lancer le serveur de développement

```bash
python manage.py runserver
```

