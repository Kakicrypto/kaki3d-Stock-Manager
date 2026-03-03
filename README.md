# 🎯 Kaki3D — Stock Manager

Gestionnaire d'inventaire de bobines de filament pour imprimante 3D.  
Développé avec **Python**, **Streamlit**, **PostgreSQL** et intégration **NFC**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-green)

---

## ✨ Fonctionnalités

- 📦 **Inventaire** — visualisation du stock avec poids restant en temps réel
- ➕ **Ajout de bobines** — enregistrement des paramètres slicer (température, débit, Pressure Advance...)
- ✏️ **Modification** — mise à jour des paramètres d'une bobine existante
- ⚖️ **Consommation** — suivi des impressions et déduction automatique du poids
- 📡 **Scanner NFC** — identification d'une bobine par tag NFC (Android + Chrome)
- 📊 **Statistiques** — graphiques de consommation par mois, projet et matière

---

## 🛠️ Stack technique

| Outil | Rôle |
|-------|------|
| Python 3.11 | Backend |
| Streamlit | Interface web |
| PostgreSQL (Supabase) | Base de données cloud |
| psycopg2 | Connecteur Python ↔ PostgreSQL |
| Web NFC API | Lecture des tags NFC depuis le navigateur |

---

## 🚀 Installation locale

### Prérequis

- Python 3.11+
- Un compte [Supabase](https://supabase.com) (gratuit)

### 1. Clone le repo

```bash
git clone https://github.com/Kakicrypto/kaki3d-Stock-Manager.git
cd kaki3d-Stock-Manager
```

### 2. Crée un environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Installe les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configure la base de données

Crée un projet sur [Supabase](https://supabase.com) et exécute le fichier `script-creation-table-inventaire.sql` dans l'éditeur SQL de Supabase.

### 5. Configure les secrets

Crée le fichier `.streamlit/secrets.toml` (ne jamais commiter ce fichier !) :

```toml
[database]
host     = "db.XXXX.supabase.co"
dbname   = "postgres"
user     = "postgres"
password = "TON_MOT_DE_PASSE"
port     = "5432"
```

### 6. Lance l'application

```bash
streamlit run app.py
```

---

## ☁️ Déploiement sur Streamlit Cloud

1. Fork ce repo sur ton GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io)
3. Connecte ton GitHub et sélectionne le repo
4. Dans **Advanced settings → Secrets**, colle le contenu de ton `secrets.toml`
5. Clique **Deploy**

---

## 📡 Fonctionnalité NFC

La lecture NFC utilise la **Web NFC API** du navigateur.

**Compatibilité :** Android + Chrome uniquement (pas iOS, pas desktop)

**Fonctionnement :**
1. Colle un tag NFC 215 sur chaque bobine
2. Enregistre l'UID du tag dans le champ NFC lors de l'ajout de la bobine
3. Sur mobile, va dans **Scanner NFC** → clique le bouton → approche le tag
4. L'appli affiche automatiquement les infos de la bobine et permet d'enregistrer une consommation

---

## 📁 Structure du projet

```
kaki3d-Stock-Manager/
├── app.py                          # Interface Streamlit
├── action.py                       # Fonctions BDD (CRUD)
├── database.py                     # Connexion PostgreSQL
├── config_custom.py                # Configuration personnalisée
├── requirements.txt                # Dépendances Python
├── static/
│   └── nfc.html                    # Page NFC (hors iframe)
├── asset/
│   └── new_logo_kaki3d.png         # Logo
├── .streamlit/
│   ├── config.toml                 # Configuration Streamlit
│   └── secrets.toml                # 🔒 Ne pas commiter !
└── script-creation-table-inventaire.sql  # Schéma BDD
```

---

## 🗄️ Schéma de base de données

```
materials ──┐
            ├── spools ──── usage_logs
marques   ──┘
```

- **materials** : types de filament (PLA, PETG, ABS...)
- **marques** : fabricants (Prusament, Esun...)
- **spools** : bobines avec paramètres slicer
- **usage_logs** : historique des consommations

---

## 📜 Licence

MIT — voir [LICENSE](LICENSE)

---

Fait avec ❤️ par [Kakicrypto](https://github.com/Kakicrypto) dans le cadre d'une reconversion en Data/IA 🚀
