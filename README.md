```
   ____     __  .-_'''-.     .-_'''-.    ______     .-------.       ____       .-'''-. .-./`)   .---.
   \   \   /  /'_( )_   \   '_( )_   \  |    _ `''. |  _ _   \    .'  __ `.   / _     \\ .-.')  | ,_|
    \  _. /  '|(_ o _)|  ' |(_ o _)|  ' | _ | ) _  \| ( ' )  |   /   '  \  \ (`' )/`--'/ `-' \,-./  )
     _( )_ .' . (_,_)/___| . (_,_)/___| |( ''_'  ) ||(_ o _) /   |___|  /  |(_ o _).    `-'`"`\  '_ '`)
 ___(_ o _)'  |  |  .-----.|  |  .-----.| . (_) `. || (_,_).' __    _.-`   | (_,_). '.  .---.  > (_)  )
|   |(_,_)'   '  \  '-   .''  \  '-   .'|(_    ._) '|  |\ \  |  |.'   _    |.---.  \  : |   | (  .  .-'
|   `-'  /     \  `-'`   |  \  `-'`   | |  (_.\.' / |  | \ `'   /|  _( )_  |\    `-'  | |   |  `-'`-'|___
 \      /       \        /   \        / |       .'  |  |  \    / \ (_ o _) / \       /  |   |   |        \
  `-..-'         `'-...-'     `'-...-'  '-----'`    ''-'   `'-'   '.(_,_).'   `-...-'   '---'   `--------`
```

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Yggdrasil** est un gestionnaire de credentials puissant et élégant permettant d'importer, stocker et rechercher efficacement des millions de paires email:password dans une base de données PostgreSQL.

## ✨ Fonctionnalités

- 🗄️ **Import massif** : Importez des millions de credentials depuis des fichiers texte
- 🔍 **Recherche rapide** : Retrouvez instantanément un email et son mot de passe
- 🎨 **Interface colorée** : Terminal avec ASCII art et couleurs
- 🛡️ **Gestion des doublons** : Évite automatiquement les entrées en double
- 📊 **Statistiques détaillées** : Suivi de l'import avec rapports par fichier
- ✅ **Validation des données** : Filtrage des emails invalides et des données trop longues
- 🔒 **Configuration sécurisée** : Identifiants séparés du code source

## 📋 Prérequis

- Python 3.11+
- PostgreSQL 16+
- Windows / Linux / macOS

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/0x94sd/Yggdrasil.git
cd Yggdrasil
```

### 2. Installer les dépendances

```bash
pip install psycopg2 colorama
```

### 3. Installer PostgreSQL

Téléchargez et installez PostgreSQL depuis [postgresql.org](https://www.postgresql.org/download/)

### 4. Configuration

Renommez `config.example.py` en `config.py` et modifiez les paramètres :

```python
db_host = "localhost"
db_port = "5432"  # Port par défaut PostgreSQL
db_user = "postgres"
db_password = "VOTRE_MOT_DE_PASSE"
db_database = "postgres"
dossier_import = r"C:\CHEMIN\VERS\VOS\FICHIERS"
```

**⚠️ IMPORTANT : Ne commitez JAMAIS le fichier `config.py` sur GitHub !**

## 📖 Utilisation

### Lancer l'application

```bash
python yggdrasil.py
```

### Menu principal

```
[1] Créer/Réinitialiser la base de données
    └─ Créez ou réinitialisez la table credentials

[2] Importer des fichiers .txt
    └─ Importez vos fichiers au format email:password

[3] Rechercher un email
    └─ Recherchez rapidement un credential

[4] Quitter
```

### Format des fichiers d'import

Les fichiers texte doivent être au format :

```
email1@example.com:password123
email2@example.com:secret456
email3@example.com:pass789
```

- Une paire email:password par ligne
- Séparateur : `:`
- Encodage : UTF-8

## 🎯 Fonctionnalités avancées

### Gestion automatique des erreurs

- **Doublons** : Ignorés automatiquement grâce à la contrainte UNIQUE
- **Emails invalides** : Filtrés (doivent contenir `@`)
- **Données trop longues** : Ignorées (max 255 caractères)
- **Lignes mal formatées** : Sautées automatiquement

### Statistiques d'import

Après chaque import, vous obtenez un rapport détaillé :

```
RÉCAPITULATIF DES LIGNES IGNORÉES (>255 caractères)
════════════════════════════════════════════════════
file1.txt                                  :    10 lignes ignorées
file2.txt                                  :     5 lignes ignorées
════════════════════════════════════════════════════
TOTAL GLOBAL                               :    15 lignes ignorées
════════════════════════════════════════════════════
```

## 🛡️ Sécurité

### Bonnes pratiques

1. **Ne partagez JAMAIS** votre fichier `config.py`
2. **Utilisez un mot de passe fort** pour PostgreSQL
3. **Limitez l'accès** à votre base de données
4. **Sauvegardez régulièrement** vos données

### Avertissement légal

⚠️ **Ce projet est uniquement à des fins éducatives.**

L'utilisation de credentials volés ou obtenus illégalement est **illégale**. Utilisez cet outil uniquement avec :

- Vos propres données
- Des données de test
- Des données pour lesquelles vous avez l'autorisation

L'auteur décline toute responsabilité en cas d'utilisation abusive.

## 🏗️ Architecture

```
Yggdrasil/
├── yggdrasil.py           # Application principale
├── config.py              # Configuration (NON commité)
├── config.example.py      # Template de configuration
├── .gitignore             # Fichiers à ignorer
└── README.md              # Documentation
```

### Structure de la base de données

```sql
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
```

## 🐛 Dépannage

### Erreur de connexion PostgreSQL

```
psycopg2.OperationalError: could not connect to server
```

**Solution :** Vérifiez que PostgreSQL est bien démarré et que les identifiants dans `config.py` sont corrects.

### Erreur d'encodage

```
UnicodeDecodeError: 'charmap' codec can't decode
```

**Solution :** Les fichiers sont automatiquement ouverts en UTF-8 avec `errors='ignore'`.

### Table existe déjà

**Solution :** Utilisez l'option 1 du menu pour réinitialiser la base de données.

## 📊 Performance

- **Import** : ~50 000 - 100 000 lignes/seconde (selon matériel)
- **Recherche** : < 1ms pour une recherche exacte
- **Capacité** : Testé jusqu'à 100M+ de credentials

## 📝 TODO

- [ ] Interface web
- [ ] Chiffrement des mots de passe stockés

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**Keryan** - [@0x94sd](https://github.com/0x94sd)

---

⭐ Si ce projet vous a été utile, n'oubliez pas de lui donner une étoile sur GitHub !
