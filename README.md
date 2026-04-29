# 🎯 Kaki3D — Stock Manager

Gestionnaire d'inventaire de bobines de filament pour imprimante 3D.  
Développé avec **Python**, **Streamlit**, **PostgreSQL** et intégration **NFC**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-green)

🌐 **Application en ligne :** https://kaki3d-stock-manager.streamlit.app

---

## ✨ Fonctionnalités

- 📦 **Inventaire** — visualisation du stock avec poids de filament restant en temps réel (graphiques donut + filtre couleur)
- ➕ **Ajout de bobines** — enregistrement des paramètres slicer (température, débit, Pressure Advance...) + gestion de la tare du support
- ✏️ **Modification** — mise à jour des paramètres d'une bobine existante
- ⚖️ **Consommation** — saisie par pesée à la balance, calcul automatique du poids consommé par différence
- 📡 **Scanner NFC** — identification d'une bobine par tag NFC (Android + Chrome)
- 📊 **Statistiques** — graphiques de consommation par mois, projet et matière

---

## 🛠️ Stack technique

| Outil | Rôle |
|-------|------|
| Python 3.11 | Backend |
| Streamlit 1.54 | Interface web |
| PostgreSQL (Supabase) | Base de données cloud |
| psycopg2 | Connecteur Python ↔ PostgreSQL |
| Plotly Express | Graphiques interactifs |
| Web NFC API | Lecture des tags NFC depuis le navigateur |
| GitHub Pages | Hébergement page NFC statique |

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

> ⚠️ **Important** : utilise la méthode de connexion **Transaction Pooler** (pas Session Pooler) pour la compatibilité avec Streamlit Cloud.

Dans les paramètres de connexion Supabase :
1. Va dans **Project Settings → Database**
2. Sélectionne **Transaction pooler**
3. Le port doit être **6543** (et non 5432)

### 5. Configure les secrets

Crée le fichier `.streamlit/secrets.toml` (⚠️ ne jamais commiter ce fichier !)

```toml
[database]
host     = "aws-0-xx-xxxx-x.pooler.supabase.com"
dbname   = "postgres"
user     = "postgres.xxxxxxxx"
password = "TON_MOT_DE_PASSE"
port     = "6543"
```

### 6. Personnalise ta configuration

Dans `config_custom.py` :
```python
pseudo = "TonPseudo"
```

Dans `.streamlit/config.toml`, tu peux ajuster les couleurs du thème :
```toml
[theme]
primaryColor = "#00FFC8"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#161B22"
textColor = "#E6EDF3"
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

---

## 📡 Fonctionnalité NFC

La lecture NFC utilise la **Web NFC API** du navigateur.

**Compatibilité :** Android + Chrome uniquement (pas iOS, pas desktop)

**Pourquoi une page GitHub Pages ?**  
Streamlit injecte ses pages dans un `iframe`, ce qui bloque la Web NFC API. La solution : une page HTML statique hébergée hors iframe sur GitHub Pages, qui redirige vers Streamlit après le scan avec l'UID en paramètre d'URL.

**Fonctionnement :**
1. Colle un tag NFC 215 sur chaque bobine
2. Enregistre l'UID du tag dans le champ NFC lors de l'ajout de la bobine
3. Sur mobile, va dans **Scanner NFC** → clique le bouton → approche le tag
4. L'appli affiche automatiquement la fiche bobine et permet d'enregistrer une consommation

**Fallback :** saisie manuelle de l'UID disponible pour desktop, iOS ou lecteur USB HID.

---

## ⚖️ Logique de consommation

Le suivi du filament repose sur la **pesée à la balance** :

1. Avant la première impression, on connaît le poids initial (`initial_weight`) et la tare du support (`poids_bobine` via la table `bobine_vide`).
2. Après chaque impression, on pèse la bobine et on saisit le poids mesuré (`poids_pesé`).
3. Le poids consommé est calculé automatiquement : `poids_consommé = dernière_pesée - poids_actuel`.

Cette approche est plus précise que saisir directement les grammes consommés estimés par le slicer.

---

## 📁 Structure du projet

```
kaki3d-Stock-Manager/
├── app.py                                # Interface Streamlit principale
├── action.py                             # Fonctions CRUD base de données (avec docstrings)
├── database.py                           # Connexion PostgreSQL via secrets
├── config_custom.py                      # Configuration personnalisée (pseudo)
├── requirements.txt                      # Dépendances Python
├── nfc.html                              # Page NFC (GitHub Pages)
├── static/
│   └── nfc.html                          # Copie page NFC (static serving Streamlit)
├── asset/
│   └── new_logo_kaki3d.png               # Logo
├── .streamlit/
│   ├── config.toml                       # Thème + static serving
│   └── secrets.toml                      # 🔒 Ne pas commiter !
└── script-creation-table-inventaire.sql  # Schéma BDD complet
```

---

## 🗄️ Schéma de base de données

```
materials ──┐
            ├── spools ──── usage_logs
marques   ──┘    │
                 └── bobine_vide
```

| Table | Rôle |
|-------|------|
| `materials` | Types de filament (PLA, PETG, ABS...) |
| `marques` | Fabricants (Prusament, Esun...) |
| `bobine_vide` | Modèles de support avec leur poids de tare |
| `spools` | Bobines avec paramètres slicer + référence au support |
| `usage_logs` | Historique des consommations (poids pesé + poids consommé) |

---

## 🔒 Sécurité

- Requêtes SQL 100% paramétrées (`%s`) — pas d'injection SQL possible
- Credentials dans `st.secrets` uniquement, jamais en dur dans le code
- `secrets.toml` dans `.gitignore`
- Whitelist `TABLES_AUTORISEES` dans `get_or_create_id()` pour les insertions dynamiques
- ⚠️ RLS à activer sur toute les tables avec :
        ✅ RLS activé sur toutes les tables
        ✅ bobine_vide — SELECT pour tous
        ✅ marques — SELECT pour tous + ALL pour service_role
        ✅ spools, usage_logs, materials — ALL pour service_role


---

## 📜 Licence

MIT — voir [LICENSE](LICENSE)

---

Fait avec ❤️ par [Kakicrypto](https://github.com/Kakicrypto) pour tous les maker un peu fou 🚀