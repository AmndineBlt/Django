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

## 🛠️ Étape 2 — Configurer PostgreSQL avec Django

### 2.1 — Installer PostgreSQL localement

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2.2 — Créer une base de données pour le projet

```bash
# Se connecter au terminal PostgreSQL
sudo -u postgres psql
```

```sql
-- Créer la base
CREATE DATABASE biblio_db;

-- Créer un utilisateur
CREATE USER biblio_user WITH PASSWORD 'biblio_pass';

-- Donner les droits sur la base
GRANT ALL PRIVILEGES ON DATABASE biblio_db TO biblio_user;

-- Quitter
\q
```

### 2.3 — Installer l’adaptateur PostgreSQL pour Django

```bash
pip install psycopg2-binary
```

### 2.4 — Configurer Django pour utiliser PostgreSQL

On ouvre le fichier `biblio_backend/settings.py`, et cherche la partie `DATABASES` :

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblio_db',
        'USER': 'biblio_user',
        'PASSWORD': 'biblio_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2.5 — Appliquer les migrations initiales

```bash
python manage.py migrate
```
Cela va créer les tables de base (auth, admin, sessions, etc.) dans ta base PostgreSQL.

## Étape 3 — Créer une application Django : `library`

### 🧠 Cours express — C’est quoi une "app" Django ?

Django est structuré autour de la notion de projet (ton backend global) et de "apps" (des modules réutilisables).

  Une app = un composant autonome de ton projet, avec ses propres modèles, vues, routes, etc.

Exemples d’apps dans un projet réel :

  library → gère les livres, listes de lecture
  users → gère les utilisateurs
  comments → gère les commentaires
  payments → gère les paiements...

Tu peux avoir plusieurs apps dans un projet Django.

### 3.1 — Créer l’app `library`

A la racine du projet
```bash
python manage.py startapp library
```
