# 🚀 Projet : Gestionnaire de Stock Filament Kaki3D

🧑‍💻 **Développeur :** Quentin (Data Analyst / Dev IA en reconversion)  
📅 **Dernière mise à jour :** Avril 2026

---

## ✅ PHASE 1 : Fondations & Base de Données (Terminé)

- [x] Configuration de PostgreSQL via Supabase (cloud).
- [x] Création du schéma relationnel (Tables : `spools`, `marques`, `materials`, `usage_logs`).
- [x] Connexion Python ↔ SQL sécurisée dans `database.py` via `st.secrets`.
- [x] Résolution des problèmes d'encodage UTF-8.
- [x] Migration vers Transaction Pooler (port 6543) pour compatibilité Streamlit Cloud (IPv4).
- [x] Ajout table `bobine_vide` pour gérer la tare du support par marque/modèle.
- [x] Mise à jour schéma : `usage_logs` avec `poids_pese` + `poids_consomme`, `spools` avec `id_bobine_vide`.

---

## ✅ PHASE 2 : Interface Streamlit & Navigation (Terminé)

- [x] Mise en place de la Sidebar avec navigation par menus (radio).
- [x] Affichage de l'inventaire sous forme de tableau (DataFrame pandas).
- [x] Intégration visuelle des jauges de stock (graphiques donut Plotly).
- [x] Filtre couleur dans la sidebar de l'inventaire.
- [x] Header personnalisé avec logo et pseudo configurable (`config_custom.py`).
- [x] Thème sombre néon configuré dans `.streamlit/config.toml`.

---

## ✅ PHASE 3 : CRUD Complet (Terminé)

- [x] Formulaire d'ajout complet avec tous les paramètres slicer (Temp, PA, Débit, vitesse...).
- [x] Fonction `get_or_create_id` : création automatique d'une marque ou matière inexistante.
- [x] Menu "Modifier une bobine" : mise à jour de tous les paramètres slicer.
- [x] Menu "Consommation" : saisie par pesée (poids mesuré à la balance), calcul automatique du poids consommé via `get_derniere_pesee`.
- [x] Gestion du type de bobine vide (`bobine_vide`) à la création et modification.
- [x] Docstrings complets sur toutes les fonctions de `action.py` (Google Style).

---

## ✅ PHASE 4 : Intégration NFC & Hardware (Terminé)

- [x] Lecture UID NFC via Web NFC API (Android + Chrome uniquement).
- [x] Page statique `nfc.html` hébergée sur GitHub Pages (contourne la limite iframe de Streamlit).
- [x] Redirection automatique vers Streamlit avec l'UID via query params.
- [x] Affichage fiche bobine complète après scan + formulaire de consommation direct.
- [x] Redirection vers page "Ajouter" si UID non reconnu + pré-remplissage du champ NFC.
- [x] Fallback saisie manuelle (compatible desktop, iOS, lecteur USB HID).

---

## ✅ PHASE 5 : Statistiques & Déploiement (Terminé)

- [x] Graphique stock par matière (bar chart Plotly).
- [x] Graphique consommation par projet (top 6, trié DESC).
- [x] Graphique consommation dans le temps (line chart avec axe mensuel).
- [x] Déploiement Streamlit Cloud : https://kaki3d-stock-manager.streamlit.app
- [x] Versioning GitHub avec protection branche `main` (PR obligatoire).

---

## 🛠️ EN COURS / À FAIRE — Court terme

- [ ] Phase bêta test — correction des retours utilisateurs.
- [ ] Correction script SQL pour nouveaux utilisateurs (syntaxe `numeric` + table `bobine_vide`).
- [ ] Améliorer la navigation NFC (éviter le passage par l'inventaire au retour).
- [ ] Mettre à jour README avec infos connexion Transaction Pooler.

---

## 📊 À FAIRE — Moyen terme

- [ ] Système d'authentification multi-utilisateurs.
- [ ] Enrichir les statistiques : filtres par période, export CSV.
- [ ] Améliorer l'UX mobile.
- [ ] Tests unitaires sur les fonctions `action.py`.
- [ ] Alertes stock bas : notification quand il reste moins de X grammes.

---

## 🤖 À FAIRE — Long terme (IA)

- [ ] Module IA : prédire si le stock est suffisant pour un fichier G-Code donné (analyse du poids estimé par le slicer).

---

## 📝 Notes & Rappels Techniques

- 💡 **Encodage** : toujours garder `# -*- coding: utf-8 -*-` en haut des fichiers Python.
- 💡 **Poids** : `initial_weight` = poids total bobine pleine. `poids_bobine` = tare du support vide. Filament disponible = `initial_weight - poids_bobine`.
- 💡 **Consommation** : on pèse la bobine après impression → `poids_consomme = derniere_pesee - poids_actuel`.
- 💡 **SQL** : toujours utiliser des requêtes paramétrées (`%s`) — jamais de f-string avec des données utilisateur.
- 💡 **Connexion** : chaque fonction de `action.py` ouvre et ferme sa propre connexion dans un `finally`.