🚀 Projet : Gestionnaire de Stock Filament Kaki3D
🧑‍💻 Développeur : Quentin (Data Analyst / Dev IA en reconversion)
📅 État d'avancement au : 23 Février 2026
✅ PHASE 1 : Fondations & Base de Données (Terminé)
[x] Configuration de PostgreSQL.

[x] Création du schéma relationnel (Tables : spools, marques, materials, usage_logs).

[x] Connexion Python <-> SQL sécurisée dans database.py.

[x] Résolution des problèmes d'encodage (le fameux bug UTF-8).

✅ PHASE 2 : Interface Streamlit & Navigation (Terminé)
[x] Mise en place de la Sidebar (barre latérale).

[x] Système de navigation par menus (radio).

[x] Affichage de l'inventaire sous forme de tableau (dataframe).

[x] Intégration visuelle des jauges de stock (barres de progression).

✅ PHASE 3 : Automatisation de la Saisie (En cours...)
[x] Formulaire d'ajout complet avec tous les paramètres techniques (Temp, PA, Débit...).

[x] Fonction "Intelligente" get_or_create_id : Ajout automatique d'une marque ou matière si elle n'existe pas.

[x] Action immédiate : Finaliser le menu ⚙️ Modifier une bobine pour corriger des erreurs de saisie.

[ ] Ajout de la fonction consomation .

[ ] Ajout du poids total restant (voir par couleur )

🛠️ PHASE 4 : Intégration NFC & Hardware (Prochaine étape)
[ ] Lecture de l'UID NFC pour identifier une bobine instantanément.

[ ] Affichage d'un "Dashboard Flash" dès qu'une bobine est scannée.

[ ] Automatisation du curseur dans le champ de recherche pour un scan fluide.

📊 PHASE 5 : Analyse de Données & IA (Le cœur du métier)
[ ] Création des graphiques de consommation (Poids utilisé vs Temps).

[ ] Alertes stock bas : Notifier quand il reste moins de X grammes.

[ ] Module IA : Prédire si le stock est suffisant pour un fichier G-Code donné (en analysant le poids estimé par le slicer).

📝 Notes & Rappels Techniques
💡 Rappel Encodage : Toujours garder # -*- coding: utf-8 -*- en haut des fichiers.
💡 Données : Poids Initial = Filament seul (1000g). Poids Bobine Vide = Tare du support.
💡 SQL : Toujours utiliser des requêtes paramétrées (%s) pour éviter que la base ne crash à cause d'un caractère spécial.