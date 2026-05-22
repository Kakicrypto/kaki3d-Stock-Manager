# 🚀 Roadmap — Kaki3D Stock Manager

**Développeur :** Quentin (Data Analyst / Dev IA en reconversion)  
**Dernière mise à jour :** Mai 2026

---

## ✅ PHASE 1 — Fondations & Base de Données *(Terminé)*

- [x] Configuration PostgreSQL (local → Supabase cloud)
- [x] Schéma relationnel : `spools`, `marques`, `materials`, `usage_logs`
- [x] Connexion Python ↔ SQL sécurisée (`database.py` + `st.secrets`)
- [x] Migration vers Transaction Pooler (IPv4, port 6543) pour Streamlit Cloud
- [x] RLS désactivé sur toutes les tables
- [x] Résolution bug encodage UTF-8
- [x] Script SQL `script-creation-table-inventaire.sql` pour nouveaux utilisateurs

---

## ✅ PHASE 2 — Interface Streamlit & Navigation *(Terminé)*

- [x] Sidebar + système de navigation par menus (`radio`)
- [x] Affichage inventaire : cards avec barres de progression + tableau DataFrame
- [x] Header personnalisé avec logo et pseudo (`config_custom.py`)
- [x] Thème sombre néon configuré (`.streamlit/config.toml`)

---

## ✅ PHASE 3 — CRUD Complet *(Terminé)*

- [x] Formulaire d'ajout de bobine avec tous les paramètres slicer
- [x] Fonction `get_or_create_id` — création automatique marque/matière si inexistante
- [x] Correction bug : matière non sauvegardée au submit (`session_state`)
- [x] Formulaire de modification de bobine
- [x] Enregistrement des consommations (`usage_logs`) + déduction poids restant
- [x] Champ NFC optionnel (`nullable` après correction BDD)

---

## ✅ PHASE 4 — Intégration NFC *(Terminé)*

- [x] Page NFC statique `nfc.html` hébergée sur GitHub Pages (contourne la limite iframe Streamlit)
- [x] Lecture UID NFC via Web NFC API (Android Chrome uniquement)
- [x] Redirection automatique vers Streamlit avec UID via query params
- [x] Affichage fiche bobine complète après scan
- [x] Formulaire de consommation directement depuis le scan
- [x] Redirection vers formulaire Ajout si UID non reconnu + pré-remplissage NFC
- [x] Fallback saisie manuelle (desktop, iOS, lecteur USB HID)
- [x] Correction redirection post-scan (interception `query_params` en tête d'`app.py`)

---

## ✅ PHASE 5 — Statistiques *(Terminé)*

- [x] Graphique stock par matière (bar chart Plotly)
- [x] Graphique consommation par projet (top 6, trié DESC)
- [x] Graphique consommation dans le temps (line chart, axe mensuel)
- [x] Gestion données vides (`df.empty` check)

---

## ✅ PHASE 6 — Déploiement & Sécurité *(Terminé)*

- [x] Déploiement Streamlit Cloud 
- [x] CI/CD automatique depuis branche `main` GitHub
- [x] Protection branche `main` via Ruleset (PR obligatoire)
- [x] Workflow : feature branches → PR → merge main
- [x] Requêtes SQL 100% paramétrées (anti-injection)
- [x] Whitelist `TABLES_AUTORISEES` dans `get_or_create_id()`
- [x] `requirements.txt` nettoyé (outils dev retirés)
- [x] README complet avec instructions d'installation

---

## 🔄 EN COURS

- [ ] Phase bêta test 
- [ ] Correction script SQL pour nouveaux utilisateurs (syntaxe `numeric`)

---

## 📋 À FAIRE — Court terme

- [x] Améliorer la navigation post-scan NFC (éviter le passage par l'inventaire au retour)
- [ ] Support iOS via lecteur NFC USB HID (saisie automatique dans le champ texte)
- [x] Supprimer le `st.write(f"DEBUG id_mat = {id_mat}")` laissé dans le formulaire d'ajout

---

## ⚖️ PHASE 7 — KakiScale : Balance Connectée *(À venir)*

> Inspiré du projet PandaBalance v2 (MakerWorld), entièrement adapté pour s'intégrer nativement à Kaki3D.  
> **Hardware cible :** ESP32 + cellule de charge 5kg + HX711 + lecteur NFC PN532 (I²C) + boîtier imprimé 3D.  
> **Principe :** poser une bobine sur la balance → l'ESP32 lit le NFC + pèse → envoie les données à Kaki3D automatiquement.

### 7.1 — Hardware & Firmware ESP32
- [x] Commande composants : ESP32, cellule de charge 5kg, module HX711, PN532 NFC
- [x] Impression 3D du boîtier (adapter le design PandaBalance v2)
- [x] Câblage et test bench : HX711 → lecture poids brut en Serial Monitor
- [x] Calibration de la cellule de charge (tare + facteur d'échelle)
- [x] Intégration PN532 : lecture UID NFC depuis l'ESP32 via I²C
- [x] Calcul poids filament réel : `poids_total_mesuré - poids_bobine_vide`
- [x] Connexion WiFi et envoi HTTP POST (JSON) vers l'API Kaki3D

### 7.2 — API REST côté Kaki3D
- [ ] Créer un endpoint `/api/scale` recevant `{ uid, poids_mesure }` depuis l'ESP32
- [ ] Identifier la bobine via l'UID → récupérer `empty_spool_weight` depuis Supabase
- [ ] Ajouter une colonne `derniere_pesee` + `date_pesee` dans la table `spools`
- [ ] Sécuriser l'endpoint avec une clé API partagée (header `X-Api-Key`)

### 7.3 — Refonte de la mesure du poids restant
- [ ] Afficher deux sources dans l'inventaire : poids calculé (actuel) vs poids mesuré (balance)
- [ ] Bouton "Recaler" : synchroniser le poids calculé sur le poids mesuré
- [ ] Horodater chaque pesée et l'afficher dans la fiche bobine
- [ ] Gérer le cas bobine inconnue : redirection vers formulaire d'ajout avec NFC pré-rempli

### 7.4 — UX & Affichage Streamlit
- [ ] Nouvelle section "Balance" dans la sidebar
- [ ] Affichage de la dernière pesée en temps réel (polling léger)
- [ ] Indicateur d'écart : alerte visuelle si dérive entre poids calculé et poids mesuré > seuil configurable

---

## 🗺️ À FAIRE — Moyen terme

- [ ] Système d'authentification (multi-utilisateurs sur instance partagée)
- [ ] Enrichir les statistiques (filtres par période, export CSV)
- [ ] Améliorer l'UX mobile (responsive)
- [ ] Tests unitaires sur les fonctions `action.py`
- [ ] Alertes stock bas : notification quand il reste moins de X grammes
- [ ] Ajout du coût d'achat et integration aux statistiques

---

## 🤖 À FAIRE — Long terme (IA)

- [ ] Module IA : prédire si le stock est suffisant pour un fichier G-Code donné
- [ ] Analyse poids estimé par le slicer vs poids réel mesuré par la balance
- [ ] Tableau de bord analytique avancé (tendances, prévisions)
- [ ] Détection automatique des anomalies de consommation (dérive poids calculé vs mesuré)

---

## 📝 Notes techniques

- Toujours garder `# -*- coding: utf-8 -*-` en haut des fichiers Python
- Poids Initial = filament seul (1000g) / Poids Bobine Vide = tare du support
- Toujours utiliser des requêtes paramétrées (`%s`) — jamais de concaténation de strings en SQL
- Connexion via Transaction Pooler Supabase (port 6543) — obligatoire sur Streamlit Cloud
- ESP32 : utiliser `HTTPClient` (Arduino) pour les appels REST, `ArduinoJson` pour sérialiser le payload
