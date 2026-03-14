# 🎯 Kaki3D — Stock Manager

Gestionnaire d'inventaire de bobines de filament pour imprimante 3D.  
Développé avec **Python**, **Streamlit**, **PostgreSQL** et intégration **NFC**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-green)
![Déployé](https://img.shields.io/badge/Déployé-Streamlit%20Cloud-brightgreen)

---

## ✨ Fonctionnalités

- 📦 **Inventaire** — visualisation du stock avec poids restant en temps réel (cards + tableau)
- ➕ **Ajout de bobines** — enregistrement des paramètres slicer (température, débit, Pressure Advance...)
- ✏️ **Modification** — mise à jour des paramètres d'une bobine existante
- ⚖️ **Consommation** — suivi des impressions et déduction automatique du poids
- 📡 **Scanner NFC** — identification d'une bobine par tag NFC (Android + Chrome)
- 📊 **Statistiques** — graphiques de consommation par mois, projet et matière (Plotly)

---

## 🛠️ Stack technique

| Outil | Rôle |
|-------|------|
| Python 3.11 | Backend |
| Streamlit 1.54 | Interface web |
| PostgreSQL via Supabase | Base de données cloud |
| psycopg2 | Connecteur Python ↔ PostgreSQL |
| Plotly Express | Graphiques statistiques |
| Web NFC API | Lecture des tags NFC depuis le navigateur |
| GitHub Pages | Hébergement de la page NFC statique |

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

> ⚠️ **Important** : Change la méthode de connexion en **Transaction Pooler** (port 6543) — nécessaire pour Streamlit Cloud qui utilise uniquement IPv4.

Récupère tes identifiants de connexion depuis le dashboard Supabase :
- Host
- User (`postgres.xxxxx`)
- Password
- Port (`6543`)

### 5. Configure les secrets

Crée le fichier `.streamlit/secrets.toml` (⚠️ ne jamais commiter ce fichier !)

```toml
[database]
host     = "aws-0-xx-xxxx-x.pooler.supabase.com"
dbname   = "postgres"
user     = "postgres.xxxxx"
password = "TON_MOT_DE_PASSE"
port     = "6543"
```

### 6. Personnalisation

Dans `config_custom.py`, remplace le pseudo par le tien :

```python
pseudo = "TonPseudo"
```

Dans `.streamlit/config.toml`, tu peux ajuster les couleurs du thème :

```toml
[theme]
primaryColor = "#00FFC8"             # Vert néon
backgroundColor = "#0E1117"          # Fond sombre
secondaryBackgroundColor = "#161B22" # Widgets
textColor = "#E6EDF3"                # Texte clair
font = "sans serif"
```

### 7. Lance l'application

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

🌐 Application déployée : [kaki3d-stock-manager.streamlit.app](https://kaki3d-stock-manager.streamlit.app)

---

## 📡 Fonctionnalité NFC

La lecture NFC utilise la **Web NFC API** du navigateur.

**Compatibilité :** Android + Chrome uniquement (pas iOS, pas desktop)

> La page NFC est hébergée sur GitHub Pages (hors iframe Streamlit) car la Web NFC API ne fonctionne pas dans un contexte iframe.

**Fonctionnement :**
1. Colle un tag NFC 215 sur chaque bobine
2. Enregistre l'UID du tag dans le champ NFC lors de l'ajout de la bobine
3. Sur mobile, va dans **Scanner NFC** → clique le bouton → approche le tag
4. L'appli affiche automatiquement les infos de la bobine et permet d'enregistrer une consommation
5. Si l'UID est inconnu → redirection automatique vers le formulaire d'ajout avec l'UID pré-rempli

📄 Page NFC statique : [kakicrypto.github.io/kaki3d-Stock-Manager/nfc.html](https://kakicrypto.github.io/kaki3d-Stock-Manager/nfc.html)

**Fallback :** saisie manuelle de l'UID disponible (compatible desktop, iOS, lecteur USB HID)

---

## 📁 Structure du projet

```
kaki3d-Stock-Manager/
├── app.py                                # Interface Streamlit principale
├── action.py                             # Fonctions CRUD base de données
├── database.py                           # Connexion PostgreSQL via secrets
├── config_custom.py                      # Personnalisation (pseudo)
├── requirements.txt                      # Dépendances Python
├── nfc.html                              # Page NFC (déployée sur GitHub Pages)
├── static/
│   └── nfc.html                          # Copie page NFC (static serving Streamlit)
├── asset/
│   └── new_logo_kaki3d.png               # Logo
├── .streamlit/
│   ├── config.toml                       # Thème + static serving
│   └── secrets.toml                      # 🔒 Ne pas commiter !
└── script-creation-table-inventaire.sql  # Schéma BDD
```

---

## 🗄️ Schéma de base de données

```
materials ──┐
            ├── spools ──── usage_logs
marques   ──┘
```

| Table | Rôle |
|-------|------|
| `materials` | Types de filament (PLA, PETG, ABS...) |
| `marques` | Fabricants (Prusament, Esun...) |
| `spools` | Bobines avec paramètres slicer + NFC ID |
| `usage_logs` | Historique des consommations par projet |

---

## 🔒 Sécurité

- Requêtes SQL 100% paramétrées (`%s`) — zéro injection SQL
- Credentials dans `st.secrets` — jamais en dur dans le code
- `secrets.toml` dans `.gitignore`
- Whitelist `TABLES_AUTORISEES` dans `get_or_create_id()`

---

## 📜 Licence

MIT — voir [LICENSE](LICENSE)

---

Fait avec ❤️ par [Kakicrypto](https://github.com/Kakicrypto) dans le cadre d'une reconversion en Data/IA 🚀
