# -*- coding: utf-8 -*-
import psycopg2
from database import get_connection #on importe la fonction du fichier database
from psycopg2.extras import RealDictCursor
connexion = get_connection()

#fonction d'ajout d'une marque 
def add_marque(nom_marque):
    if connexion:
        try:
            with connexion: # Gère le commit/rollback automatique
                with connexion.cursor() as curs:# gere la fermeture du curseur
                    #on utilise le placeholder %s pour la securite
                    requete = "INSERT INTO marques (nom_marques) VALUES (%s);"
                    curs.execute(requete, (nom_marque,))
                print (f"Marque '{nom_marque}' ajoutee avec succes!")
        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}")
        finally:
            connexion.close() # On n'oublie pas de rendre la connexion au serveur

# Test de la fonction
if __name__ == "__main__":
    add_marque("Prusament")

def add_spool(nfc_id, color_name, initial_weight, empty_weight, diametre, 
              temp_imp, temp_table, debit, pressure_adv, vit_max,vit_imp,
              id_marques, id_materials):
    connexion = get_connection()
    if connexion:
        try:
            with connexion: # Commit automatique ici
                with connexion.cursor() as curs:
                    requete = """
                    INSERT INTO public.spools (
                        nfc_id, 
                        color_name, 
                        initial_weight, 
                        empty_spool_weight, 
                        diametre, 
                        temperature_imp, 
                        temperature_table, 
                        debit, 
                        pressure_advance, 
                        vit_volum_max,
                        vit_imp, 
                        id_marques, 
                        id_materials                        
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    # On crée un tuple avec TOUTES les valeurs dans le bon ordre
                    params = (
                        nfc_id, color_name, initial_weight, empty_weight, 
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

#fonction d'aggregation des bobines
def get_aggregated_inventory():
    connexion = get_connection()
    inventory = []
    if connexion:
        try:
            # On utilise RealDictCursor pour récupérer les noms des colonnes facilement
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                requete = """
                SELECT 
                    m.nom_marques, 
                    mat.type_materials,
                    s.color_name,
                    -- On somme les poids initiaux de toutes les bobines du même type
                    SUM(s.initial_weight) AS total_initial,
                    -- On calcule le reste global : Somme des initiaux - Somme de TOUS les logs
                    (SUM(s.initial_weight) - COALESCE(SUM(u.weight_used), 0)) AS total_restant
                FROM public.spools s
                JOIN public.marques m ON s.id_marques = m.id_marques
                JOIN public.materials mat ON s.id_materials = mat.id_materials
                LEFT JOIN public.usage_logs u ON s.id_spools = u.id_spools
                GROUP BY m.nom_marques, mat.type_materials, s.color_name
                ORDER BY m.nom_marques;
                """
                curs.execute(requete)
                inventory = curs.fetchall()
        except Exception as e:
            print(f"Erreur agrégation : {e}")
        finally:
            connexion.close()
    return inventory

#fonction de consomation du filament 
def usage_log (weight_used, date_print, id_spools, project_name):
    connexion = get_connection()
    if connexion:
        try: 
            with connexion:
                with connexion.cursor() as curs:
                    requete = """
                    INSERT INTO public.usage_logs (weight_used, print_date, id_spools, project_name)
                    VALUES (%s, %s, %s, %s);
                    """
                    curs.execute(requete,(weight_used, date_print, id_spools, project_name))
                    #c'est ici qu'on recuperes les donnees !
                    print(f"---{weight_used}g de {id_spools} consomme sur le projet {project_name} ---")     
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de consomation  : {e}")
            return False
        finally:
            connexion.close() # On n'oublie pas de rendre la connexion au serveur
    return False

#fonction de calcul et affichage du poids restant
def get_remaining_weight (id_bobine,):
    connexion = get_connection()
    poids = None
    if connexion:
        try:
            # On utilise le curseur "Dictionnaire" ici
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                requete = """
                SELECT s.initial_weight - COALESCE(SUM(u.weight_used), 0) AS reste
                FROM public.spools s
                LEFT JOIN public.usage_logs u ON s.id_spools = u.id_spools
                WHERE s.id_spools = %s
                GROUP BY s.initial_weight;"""
                curs.execute(requete, (id_bobine))
                resultat = curs.fetchone()
                if resultat:
                    poids = resultat['reste']
        except Exception as e:
            print(f"Erreur de calcul : {e}")
        finally:
            connexion.close()
            
    return poids

#test 
if __name__ == "__main__":
    mon_poids = get_remaining_weight(1)
    print(f"Il reste {mon_poids}g sur la bobine n°1.")

def get_inventory():
    connexion = get_connection()
    inventory = []
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                # Cette requête calcule le reste pour CHAQUE bobine de la base
                requete = """
                SELECT 
                    s.*, 
                    m.nom_marques, 
                    mat.type_materials,
                    -- Le calcul magique : poids initial moins somme des consos
                    (s.initial_weight - COALESCE(SUM(u.weight_used), 0)) AS poids_restant
                FROM public.spools s
                JOIN public.marques m ON s.id_marques = m.id_marques
                JOIN public.materials mat ON s.id_materials = mat.id_materials
                LEFT JOIN public.usage_logs u ON s.id_spools = u.id_spools
                GROUP BY s.id_spools, m.id_marques, m.nom_marques, mat.id_materials, mat.type_materials
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
    connexion = get_connection()
    if connexion:
        try:
            with connexion.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("SELECT id_materials, type_materials FROM public.materials ORDER BY type_materials;")
                return curs.fetchall()
        finally:
            connexion.close()
    return []

#creation d'un champ inexistant (table marque ou matiere)
def get_or_create_id(table, column, value):
    """
    Vérifie si une valeur existe dans une table (ex: 'Prusament' dans 'marques').
    Si oui, renvoie l'ID. Sinon, l'insère et renvoie le nouvel ID.
    """
    if not value: return None
    connexion = get_connection()
    if connexion:
        try:
            with connexion:
                with connexion.cursor() as curs:
                    curs.execute(f"SELECT id_{table} FROM {table} WHERE {column} ILIKE %s", (value.strip(),))
                    res = curs.fetchone()
                    if res: return res[0]
                    curs.execute(f"INSERT INTO {table} ({column}) VALUES (%s) RETURNING id_{table}", (value.strip(),))
                    return curs.fetchone()[0]
        finally: connexion.close()
    return None

def update_spool(id_spools, nfc_id, id_materials, id_marques, color_name, initial_weight, empty_spool_weight, 
                 diametre, temperature_imp, temperature_table, debit, pressure_advance, vit_volum_max):
    """
    Verifie si la bobine exisiste et permettre  
    """
    connexion = get_connection()
    if connexion:
        try:
            with connexion:
                with connexion.cursor() as curs:
                    requete = """
                    UPDATE public.spools SET
                    nfc_id = %s, id_materials = %s, id_marques = %s, color_name = %s, initial_weight = %s, 
                    empty_spool_weight = %s, diametre = %s, temperature_imp = %s, 
                    temperature_table = %s, debit = %s, pressure_advance = %s, 
                    vit_volum_max = %s
                    WHERE id_spools = %s;
                    """
                    curs.execute (requete, (nfc_id, id_materials, id_marques, color_name, initial_weight, empty_spool_weight, 
                                        diametre, temperature_imp, temperature_table, debit, 
                                        pressure_advance, vit_volum_max, id_spools))
            return True
        except Exception as e:
            print(f"Erreur Update {e}")
            return False
        finally:
            connexion.close()
    return False

#Recuperation NFC d'une bobine 

def get_spool_by_nfc(nfc_uid: str):
    """
    Recherche une bobine par son UID NFC.
    Retourne un dict (RealDict) avec toutes les infos + poids_restant,
    ou None si aucune bobine ne correspond.

    Utilisation dans app.py :
        spool = get_spool_by_nfc("04:AB:12:CD:EF:00:01")
        if spool:
            st.write(spool['nom_marques'], spool['poids_restant'])
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
                (s.initial_weight - COALESCE(SUM(u.weight_used), 0)) AS poids_restant
            FROM public.spools s
            JOIN public.marques  m   ON s.id_marques   = m.id_marques
            JOIN public.materials mat ON s.id_materials = mat.id_materials
            LEFT JOIN public.usage_logs u ON s.id_spools = u.id_spools
            WHERE s.nfc_id ILIKE %s          -- ILIKE = insensible à la casse
            GROUP BY s.id_spools, m.id_marques, m.nom_marques,
                     mat.id_materials, mat.type_materials
            LIMIT 1;
            """
            curs.execute(requete, (nfc_uid.strip(),))
            result = curs.fetchone()
            return result   # None si pas trouvé, dict sinon
    except Exception as e:
        print(f"Erreur get_spool_by_nfc : {e}")
        return None
    finally:
        connexion.close()
        
def stats ():
    connexion = get_connection()