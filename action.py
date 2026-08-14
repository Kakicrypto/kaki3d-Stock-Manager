# -*- coding: utf-8 -*-
"""
action.py — Couche d'accès aux données (DAL) pour Kaki3D Stock Manager.

Ce module regroupe toutes les fonctions CRUD (Create, Read, Update) qui
interagissent avec la base de données PostgreSQL via psycopg2.
Chaque fonction ouvre sa propre connexion et la ferme systématiquement
dans un bloc `finally`, garantissant l'absence de fuite de connexion.
"""

import psycopg2
from database import get_connection
from psycopg2.extras import RealDictCursor
import streamlit as st
import requests

# Whitelist de sécurité pour get_or_create_id
TABLES_AUTORISEES = {
    "marques": "nom_marques",
    "materials": "type_materials"
}


def add_spool(nfc_id, color_name, initial_weight, id_bobine_vide, diametre,
            temp_imp, temp_table, debit, pressure_adv, vit_max, vit_imp,
            id_marques, id_materials):
    """Insère une nouvelle bobine de filament dans la table `spools`.

    Args:
        nfc_id (str): UID du tag NFC collé sur la bobine. Peut être vide ("").
        color_name (str): Nom de la couleur du filament (ex: "Galaxy Black").
        initial_weight (float): Poids total de la bobine pleine en grammes
            (filament + support).
        id_bobine_vide (int): Clé étrangère vers la table `bobine_vide`,
            indiquant le modèle de support utilisé.
        diametre (float): Diamètre du filament en mm (ex: 1.75 ou 2.85).
        temp_imp (float): Température de la buse recommandée en °C.
        temp_table (float): Température du plateau recommandée en °C.
        debit (float): Débit d'extrusion en pourcentage (ex: 100.0).
        pressure_adv (float): Valeur de Pressure Advance pour Klipper/Marlin.
        vit_max (int): Vitesse volumétrique maximale en mm³/s.
        vit_imp (int): Vitesse d'impression recommandée en mm/s.
        id_marques (int): Clé étrangère vers la table `marques`.
        id_materials (int): Clé étrangère vers la table `materials`.

    Returns:
        bool: True si l'insertion a réussi, False en cas d'erreur SQL
            ou si la connexion est indisponible.
    """
    connexion = get_connection()
    nfc_id = nfc_id if nfc_id else ""
    if connexion:
        try:
            with connexion:
                with connexion.cursor() as curs:
                    requete = """
                    INSERT INTO public.spools (
                        nfc_id, color_name, initial_weight, id_bobine_vide,
                        diametre, temperature_imp, temperature_table, debit,
                        pressure_advance, vit_volum_max, vit_imp, id_marques, id_materials
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    params = (
                        nfc_id, color_name, initial_weight, id_bobine_vide,
                        diametre, temp_imp, temp_table, debit,
                        pressure_adv, vit_max, vit_imp, id_marques, id_materials
                    )
                    curs.execute(requete, params)
            return True
        except Exception as e:
            print(f"Erreur SQL lors de l'ajout : {e}")
            return False
        finally:
            connexion.close()
    return False


def get_aggregated_inventory():
    """Récupère un résumé agrégé du stock, groupé par marque / matière / couleur.

    Calcule pour chaque groupe :
    - le poids de filament initial (poids total − poids du support vide)
    - le poids de filament restant (initial − somme des consommations)

    Returns:
        list[RealDictRow]: Liste de dictionnaires contenant les clés
            `nom_marques`, `type_materials`, `color_name`, `poids_bobine`,
            `poids_filament_initial`, `poids_filament_restant`.
            Retourne une liste vide en cas d'erreur ou si la BDD est vide.
    """
    connexion = get_connection()
    inventory = []
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                requete = """
                WITH conso AS (
                    SELECT id_spools, SUM(poids_consomme) as total_consomme
                    FROM usage_logs
                    GROUP BY id_spools
                )
                SELECT 
                    c.total_consomme ,
                    m.nom_marques, 
                    mat.type_materials,
                    s.color_name,
                    bv.poids_bobine,
                    (SUM(s.initial_weight - bv.poids_bobine)) as poids_filament_initial,
                    (SUM(s.initial_weight - bv.poids_bobine) - COALESCE(c.total_consomme, 0)) AS poids_filament_restant
                FROM spools s
                JOIN public.marques m ON s.id_marques = m.id_marques
                JOIN public.materials mat ON s.id_materials = mat.id_materials
                LEFT JOIN public.bobine_vide bv on s.id_bobine_vide = bv.id_bobine_vide
                LEFT JOIN conso c ON s.id_spools = c.id_spools
                GROUP BY m.nom_marques, mat.type_materials, s.color_name,bv.poids_bobine,c.total_consomme
                HAVING (SUM(s.initial_weight - bv.poids_bobine) - COALESCE(c.total_consomme, 0)) > 5
                ORDER BY m.nom_marques
                
                """


                curs.execute(requete)
                inventory = curs.fetchall()
        except Exception as e:
            print(f"Erreur agrégation : {e}")
        finally:
            connexion.close()
    return inventory


def usage_log(poids_pese, poids_consomme, date_print, id_spools, project_name):
    """Enregistre une consommation de filament dans la table `usage_logs`.

    Deux valeurs de poids sont stockées : le poids pesé directement sur
    la balance (bobine + filament restant), et le poids de filament
    effectivement consommé calculé par différence avec la pesée précédente.

    Args:
        poids_pese (float): Poids total mesuré à la balance en grammes
            (support + filament restant) après l'impression.
        poids_consomme (float): Poids de filament consommé en grammes
            pour cette impression.
        date_print (datetime.date): Date de l'impression.
        id_spools (int): Clé étrangère vers la bobine utilisée.
        project_name (str): Nom du projet imprimé (ex: "Calibration cube").

    Returns:
        bool: True si l'insertion a réussi, False en cas d'erreur SQL
            ou si la connexion est indisponible.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion:
                with connexion.cursor() as curs:
                    requete = """
                    INSERT INTO public.usage_logs (poids_pese, poids_consomme, print_date, id_spools, project_name)
                    VALUES (%s,%s, %s, %s, %s);
                    """
                    curs.execute(requete, (poids_pese, poids_consomme, date_print, id_spools, project_name))
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de consommation : {e}")
            return False
        finally:
            connexion.close()
    return False


def get_inventory():
    """Récupère la liste complète des bobines avec leur poids de filament restant.

    Pour chaque bobine, le poids restant est calculé en soustrayant la somme
    des consommations enregistrées au poids de filament initial
    (poids total − poids du support vide).

    Returns:
        list[RealDictRow]: Liste de dictionnaires contenant toutes les colonnes
            de `spools` enrichies de `nom_marques`, `type_materials`,
            `poids_bobine` et `poids_filament_restant`.
            Triée par `id_spools` décroissant (bobines les plus récentes en premier).
            Retourne une liste vide en cas d'erreur.
    """
    connexion = get_connection()
    inventory = []
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                requete = """
                SELECT 
                    s.*, 
                    m.nom_marques, 
                    mat.type_materials,
                    bv.poids_bobine,
                    ((s.initial_weight-bv.poids_bobine) - COALESCE(SUM(u.poids_consomme), 0)) AS poids_filament_restant
                FROM public.spools s
                JOIN public.marques m ON s.id_marques = m.id_marques
                JOIN public.materials mat ON s.id_materials = mat.id_materials
                LEFT JOIN public.usage_logs u ON s.id_spools = u.id_spools
                LEFT JOIN public.bobine_vide bv on s.id_bobine_vide = bv.id_bobine_vide
                GROUP BY s.id_spools, m.id_marques, m.nom_marques, mat.id_materials, mat.type_materials, bv.poids_bobine
                ORDER BY s.id_spools DESC;
                """
                curs.execute(requete)
                inventory = curs.fetchall()
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            connexion.close()
    return inventory


def get_all_brands():
    """Récupère toutes les marques enregistrées, triées alphabétiquement.

    Returns:
        list[RealDictRow]: Liste de dictionnaires avec les clés
            `id_marques` et `nom_marques`.
            Retourne une liste vide si la connexion échoue.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT id_marques, nom_marques FROM public.marques ORDER BY nom_marques;")
                return curs.fetchall()
        finally:
            connexion.close()
    return []


def get_all_materials():
    """Récupère tous les types de matière enregistrés, triés alphabétiquement.

    Returns:
        list[RealDictRow]: Liste de dictionnaires avec les clés
            `id_materials` et `type_materials`.
            Retourne une liste vide si la connexion échoue.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT id_materials, type_materials FROM public.materials ORDER BY type_materials;")
                return curs.fetchall()
        finally:
            connexion.close()
    return []


def get_or_create_id(table, column, value):
    """Retourne l'ID d'une valeur dans une table, en la créant si elle n'existe pas.

    Implémente un pattern "upsert léger" : cherche d'abord la valeur
    (insensible à la casse via ILIKE), et l'insère uniquement si absente.
    Protégé par une whitelist pour éviter toute injection via le nom de table.

    Args:
        table (str): Nom de la table cible. Doit être dans `TABLES_AUTORISEES`
            (`"marques"` ou `"materials"`).
        column (str): Nom de la colonne texte à rechercher / insérer.
        value (str): Valeur à rechercher ou créer (les espaces de bord sont supprimés).

    Returns:
        int | None: L'ID de la ligne existante ou nouvellement créée.
            None si `value` est vide, si la table n'est pas autorisée,
            ou si la connexion échoue.
    """
    if not value:
        return None
    if table not in TABLES_AUTORISEES:
        print(f"Table '{table}' non autorisée !")
        return None
    connexion = get_connection()
    if connexion:
        try:
            with connexion:
                with connexion.cursor() as curs:
                    curs.execute(f"SELECT id_{table} FROM {table} WHERE {column} ILIKE %s", (value.strip(),))
                    res = curs.fetchone()
                    if res:
                        return res[0]
                    curs.execute(f"INSERT INTO {table} ({column}) VALUES (%s) RETURNING id_{table}", (value.strip(),))
                    return curs.fetchone()[0]
        finally:
            connexion.close()
    return None


def update_spool(id_spools, nfc_id, id_materials, id_marques, color_name, id_bobine_vide,
                empty_spool_weight, diametre, temperature_imp, temperature_table,
                debit, pressure_advance, vit_volum_max, vit_imp=0):
    """Met à jour les paramètres d'une bobine existante dans la table `spools`.

    Tous les champs sont mis à jour en une seule requête UPDATE.
    Le poids initial (`initial_weight`) n'est pas modifiable ici par conception :
    il représente la valeur de référence à la création.

    Args:
        id_spools (int): Identifiant de la bobine à modifier.
        nfc_id (str): Nouvel UID NFC.
        id_materials (int): Nouvelle clé étrangère vers `materials`.
        id_marques (int): Nouvelle clé étrangère vers `marques`.
        color_name (str): Nouveau nom de couleur.
        id_bobine_vide (int): Nouvelle clé étrangère vers `bobine_vide`.
        empty_spool_weight (float): Poids du support vide en grammes.
        diametre (float): Diamètre du filament en mm.
        temperature_imp (float): Température de buse en °C.
        temperature_table (float): Température de plateau en °C.
        debit (float): Débit en pourcentage.
        pressure_advance (float): Valeur de Pressure Advance.
        vit_volum_max (int): Vitesse volumétrique maximale en mm³/s.
        vit_imp (int, optional): Vitesse d'impression en mm/s. Défaut : 0.

    Returns:
        bool: True si la mise à jour a réussi, False en cas d'erreur SQL
            ou si la connexion est indisponible.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion:
                with connexion.cursor() as curs:
                    requete = """
                    UPDATE public.spools SET
                        nfc_id = %s, id_materials = %s, id_marques = %s, color_name = %s,
                        id_bobine_vide =%s, empty_spool_weight = %s, diametre = %s,
                        temperature_imp = %s, temperature_table = %s, debit = %s,
                        pressure_advance = %s, vit_volum_max = %s, vit_imp = %s
                    WHERE id_spools = %s;
                    """
                    curs.execute(requete, (
                        nfc_id, id_materials, id_marques, color_name, id_bobine_vide,
                        empty_spool_weight, diametre, temperature_imp, temperature_table,
                        debit, pressure_advance, vit_volum_max, vit_imp, id_spools
                    ))
            return True
        except Exception as e:
            print(f"Erreur Update : {e}")
            return False
        finally:
            connexion.close()
    return False


def get_spool_by_nfc(nfc_uid: str):
    """Recherche une bobine par son UID NFC.

    Utilisée après un scan NFC pour afficher instantanément la fiche bobine
    et proposer un enregistrement de consommation.
    La recherche est insensible à la casse (ILIKE).

    Args:
        nfc_uid (str): UID du tag NFC lu par le navigateur
            (ex: "04:AB:12:CD:EF:00:01").

    Returns:
        RealDictRow | None: Dictionnaire contenant toutes les colonnes de
            `spools` enrichies de `nom_marques`, `type_materials`,
            `poids_bobine` et `poids_filament_restant`.
            None si aucune bobine ne correspond ou en cas d'erreur.
    """
    connexion = get_connection()
    if not connexion:
        return None
    try:
        with connexion.cursor(cursor_factory=RealDictCursor) as curs:
            requete = """
            SELECT
                s.*,
                m.nom_marques,
                mat.type_materials,
                bv.poids_bobine,
                ((s.initial_weight - bv.poids_bobine) - COALESCE(SUM(u.poids_consomme), 0)) AS poids_filament_restant
            FROM public.spools s
            JOIN public.marques m ON s.id_marques = m.id_marques 
            JOIN public.materials mat ON s.id_materials = mat.id_materials
            LEFT JOIN public.usage_logs u ON s.id_spools = u.id_spools
            LEFT JOIN public.bobine_vide bv on s.id_bobine_vide = bv.id_bobine_vide
            WHERE s.nfc_id ILIKE %s
            GROUP BY s.id_spools, m.id_marques, m.nom_marques, mat.id_materials, mat.type_materials, bv.poids_bobine
            LIMIT 1;
            """
            curs.execute(requete, (nfc_uid.strip(),))
            return curs.fetchone()
    except Exception as e:
        print(f"Erreur get_spool_by_nfc : {e}")
        return None
    finally:
        connexion.close()


def get_stats_by_month():
    """Calcule la consommation totale de filament par mois calendaire.

    Utilisée pour le graphique en courbe dans la page Statistiques.

    Returns:
        list[RealDictRow]: Liste de dictionnaires avec les clés
            `mois` (date tronquée au 1er du mois) et `total_consomme` (float).
            Triée par ordre chronologique croissant.
            Retourne une liste vide si la connexion échoue.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("""
                SELECT 
                    DATE_TRUNC('month', print_date) AS mois,
                    SUM(poids_consomme) AS total_consomme
                FROM public.usage_logs
                GROUP BY mois
                ORDER BY mois;
                """)
                return curs.fetchall()
        finally:
            connexion.close()
    return []


def get_stats_by_project():
    """Calcule la consommation totale de filament par projet, limité au top 6.

    Utilisée pour le graphique en barres "consommation par projet"
    dans la page Statistiques.

    Returns:
        list[RealDictRow]: Liste de dictionnaires avec les clés
            `project_name` (str) et `total_consomme` (float).
            Triée par consommation décroissante, maximum 6 résultats.
            Retourne une liste vide si la connexion échoue.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("""
                SELECT
                    project_name,
                    SUM(poids_consomme) AS total_consomme
                FROM public.usage_logs
                GROUP BY project_name
                ORDER BY total_consomme DESC
                LIMIT 6;
                """)
                return curs.fetchall()
        finally:
            connexion.close()
    return []


def get_stats_by_material():
    """Calcule le poids total de filament en stock par type de matière.

    Basé sur le poids restant dans les bobine ,
    ce qui représente la quantité restantes par matière.
    Utilisée pour le graphique en barres "stock par matières".

    Returns:
        list[RealDictRow]: Liste de dictionnaires avec les clés
            `type_materials` (str) et `poids_filament_restant` (float).
            Triée par poids décroissant.
            Retourne une liste vide si la connexion échoue.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("""
                WITH conso AS (
                    SELECT id_spools, SUM(poids_consomme) as total_consomme
                    FROM usage_logs
                    GROUP BY id_spools
                )
                SELECT 
                mat.type_materials,
                (SUM(s.initial_weight) - SUM(bv.poids_bobine)) as poids_filament_initial,
                (SUM(s.initial_weight - bv.poids_bobine) - COALESCE(sum(c.total_consomme), 0)) AS poids_filament_restant
                FROM public.spools s
                JOIN public.materials mat ON s.id_materials = mat.id_materials
                LEFT JOIN public.bobine_vide bv on s.id_bobine_vide = bv.id_bobine_vide
                LEFT JOIN conso c ON s.id_spools = c.id_spools
                GROUP BY mat.type_materials
                order by poids_filament_restant desc
                """)
                return curs.fetchall()
        finally:
            connexion.close()
    return []

def get_derniere_pesee(id_spools, initial_weight):
    """Récupère le dernier poids pesé enregistré pour une bobine donnée.

    Permet de pré-remplir le champ "poids pesé" dans le formulaire de
    consommation avec la valeur la plus récente. Si aucune pesée n'existe
    encore (bobine neuve), retourne le poids de filament initial
    (poids total) comme valeur de référence.

    Args:
        id_spools (int): Identifiant de la bobine concernée.
        initial_weight (float): Poids total de la bobine pleine en grammes.

    Returns:
        tuple | bool: Tuple à un élément contenant `derniere_pesee` (float)
            si la requête réussit. False en cas d'erreur SQL ou si la
            connexion est indisponible.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor() as curs:
                requete = ("""
                        SELECT COALESCE(
                        (SELECT poids_pese FROM usage_logs WHERE id_spools = %s ORDER BY print_date DESC LIMIT 1),
                        (%s)
                        ) AS derniere_pesee
                        """)
                curs.execute(requete, (id_spools, initial_weight))
                return curs.fetchone()
        except Exception as e:
            print(f"Erreur Ajout consommation : {e}")
            return False
        finally:
            connexion.close()
    return False



def get_all_bobine_vide_commune():
    """Récupère tous les modèles de support de bobine vide enregistrés via l'api  .
        les données viennent de Supabase pour que la base de données de bobine vide
        soit accessible et commune à tous les utilisateurs.

    Utilisée pour alimenter les selectbox lors de l'ajout ou de la
    modification d'une bobine, afin d'associer le bon poids de tare.

    Returns:
        list[dict]: Liste de dictionnaires avec les clés
            `type_bobine`, `poids_bobine`, `id_marques`, `nom_marques`
            et `id_bobine_vide`.
            Triée par nom de marque alphabétique.
            Retourne une liste vide si la connexion échoue.
    """
    try:
        url = st.secrets["api"]["url"]+"bobine_vide?select=id_bobine_vide,poids_bobine,type_bobine,id_marques,photo_url,marques(id_marques,nom_marques)"
        anon_key = st.secrets["api"]["anon"]
        
        response = requests.get(
            url,
            headers={
                "apikey": anon_key,
                "Authorization": "Bearer " + anon_key
            }
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.json()
    except Exception as e:
            print(f"Erreur lors de la connexion : {e}")
            return []

def get_buy_by_material():
    """Calcule le poids total de filament en stock par type de matière.

    Basé sur le poids initial des bobines (sans déduire les consommations),
    ce qui représente la quantité achetée par matière.
    Utilisée pour le graphique en barres "stock par matières".

    Returns:
        list[RealDictRow]: Liste de dictionnaires avec les clés
            `type_materials` (str) et `poids_total` (float).
            Triée par poids décroissant.
            Retourne une liste vide si la connexion échoue.
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("""
                SELECT 
                    mat.type_materials,
                    SUM(s.initial_weight) AS poids_total
                FROM public.spools s
                JOIN public.materials mat ON s.id_materials = mat.id_materials
                GROUP BY mat.type_materials
                ORDER BY poids_total DESC;
                """)
                return curs.fetchall()
        finally:
            connexion.close()
    return []