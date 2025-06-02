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
-- Créer un utilisateur
CREATE USER biblio_user WITH LOGIN PASSWORD 'biblio_pass';

-- Créer la base de données
CREATE DATABASE biblio_db WITH OWNER biblio_user;

-- Se déplacer dans la base
\c biblio_db biblio_user

-- Connexion direct
psql -d biblio_db -U biblio_user

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

## 🛠️ Étape 3 — Créer une application Django : `library`

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

### 3.2 — Déclarer l’app dans le projet

Pour que Django prenne en compte l’app, il faut l’ajouter à la config.
Ouvre biblio_backend/settings.py et dans INSTALLED_APPS, ajoute :

```py
INSTALLED_APPS = [
    # apps de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ton app perso
    'library',
]
```
### 3.3 — Vérification

Tester que tout est bien connecté :
```bash
python manage.py makemigrations
python manage.py migrate
```
Même s’il n’y a pas encore de modèle, Django garde une trace de ton app

## 🛠️ Étape 4 — Structure de la base de données

### 1.1 — Quelles sont les entités principales ?

| Entité        | Description                                                                     |
| ------------- | ------------------------------------------------------------------------------- |
| **User**      | L’utilisateur connecté (utilise `django.contrib.auth`)                          |
| **Book**      | Un livre (titre, auteur, résumé...)                                             |
| **UserList**  | Une **liste personnelle** d’un utilisateur                                      |
| **ListEntry** | Lien entre un **livre** et une **liste** (ex : "ce livre est dans mes favoris") |
| **Review**    | Un commentaire ou une note laissée par un utilisateur sur un livre              |

### 2.2 — Modèle conceptuel de données (MCD)

Les relations :
* Un utilisateur peut créer plusieurs listes (lu, à lire, favoris...)
* Une liste contient plusieurs livres, et un livre peut être dans plusieurs listes
* Un utilisateur peut noter ou commenter un livre
* Un livre peut recevoir plusieurs reviews (notes/commentaires)
* Les livres sont partagés par tous, mais les listes sont propres à chaque utilisateur

🧍 User (fourni par Django)
→ On utilisera `from django.contrib.auth.models import User`

📘 Book
```py
isbn: str
title: str
author: str
description: text
created_at: datetime
```

🗂️ UserList
```py
user: FK → User
name: str (ex: "à lire", "favoris", etc.)
created_at: datetime
```
→ Chaque utilisateur peut avoir plusieurs listes

📚 ListEntry
```py
book: FK → Book
user_list: FK → UserList
added_at: datetime
```
→ Représente un livre dans une liste précise

📝 Review
```py
user: FK → User
book: FK → Book
rating: int (1 à 5)
comment: text
created_at: datetime
```

### 2.3 — Création du modèle `Book`

```py
class Book(models.Model):
    # Title of the book (required, max 255 characters)
    title = models.CharField(max_length=255)
    # Author's name (required)
    author = models.CharField(max_length=255)
    # Short or long description of the book (optional)
    description = models.TextField(blank=True)
    # ISBN number (required, unique if provided)
    isbn = models.CharField(max_length=13, unique=True)
    # Automatically store the date the book was added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # What shows up in admin or console when we print the object
        return f"{self.title} by {self.author}"
```

### 2.4 — Appliquer les migrations

Rappel rapide : c’est quoi une migration ?
  Une migration, c’est une “traduction” de ton modèle Python (Book) vers une table SQL (dans PostgreSQL ici).

  Django garde un historique des migrations pour que tu puisses ajouter / modifier / supprimer des modèles de manière propre et traçable.

#### a. Générer les fichiers de migration

```bash
python manage.py makemigrations
```
→ Django détecte les nouveaux modèles (ici Book) et crée un fichier dans library/migrations/.

#### b. Appliquer les migrations (écrire dans PostgreSQL)

```bash
python manage.py migrate
```
→ Cela crée la vraie table library_book dans ta base PostgreSQL.

#### c. Vérification rapide

```bash
python manage.py showmigrations
```
→ Si la migration c'est bien passé on voit un [X] devant library.0001_initial

## 🛠️ Étape 5 — Configuration de l'admin

### 1.1 — Créer un superutilisateur (admin)

```bash
python manage.py createsuperuser
```

## 🛠️ Étape 6 — Les fixtures

### 1.1 — Créer un dossier pour stocker les fixtures

### 1.2 — Créer un fichier books.json

```json
[
  {
    "model": "library.book",
    "pk": 1,
    "fields": {
      "isbn": "9782070368228",
      "title": "Le Petit Prince",
      "author": "Antoine de Saint-Exupéry",
      "description": "Un conte poétique et philosophique.",
      "published": "1943",
      "page_count": 96,
      "rating": 4.8,
      "created_at": "2025-06-01T12:00:00Z"
    }
  },
]
```

```bash
python manage.py loaddata library/fixtures/books.json
```

