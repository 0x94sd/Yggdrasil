import psycopg2
import os
from colorama import Fore, Style, init
from config import db_host, db_port, db_user, db_password, db_database, dossier_import

init()  # Initialise colorama

# clear le terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def afficher_logo():
    ligne1 = "   ____     __  .-_'''-.     .-_'''-.    ______     .-------.       ____       .-'''-. .-./`)   .---.      "
    ligne2 = "   \\   \\   /  /" + Fore.MAGENTA + "'_( )_   \\   '_( )_   \\" + Fore.GREEN + "  |    _ `''. |  _ _   \\    .'  __ `.   / _     \\\\ .-.')  | ,_|      "
    ligne3 = "    \\  _. /  '|" + Fore.MAGENTA + "(_ o _)" + Fore.GREEN + "|  ' |" + Fore.MAGENTA + "(_ o _)" + Fore.GREEN + "|  ' | _ | ) _  \\| ( ' )  |   /   '  \\  \\ (`' )/`--'/ `-' \\,-./  )      "
    ligne4 = "     _" + Fore.MAGENTA + "( )" + Fore.GREEN + "_ .' . " + Fore.MAGENTA + "(_,_)" + Fore.GREEN + "/___| . " + Fore.MAGENTA + "(_,_)" + Fore.GREEN + "/___| |( ''_'  ) ||" + Fore.MAGENTA + "(_ o _)" + Fore.GREEN + " /   |___|  /  |" + Fore.MAGENTA + "(_ o _)" + Fore.GREEN + ".    `-'`\"`\\  '_ '`)    "
    ligne5 = " ___" + Fore.MAGENTA + "(_ o _)" + Fore.GREEN + "'  |  |  .-----.|  |  .-----.| . " + Fore.MAGENTA + "(_)" + Fore.GREEN + " `. || " + Fore.MAGENTA + "(_,_)" + Fore.GREEN + ".' __    _.-`   | " + Fore.MAGENTA + "(_,_)" + Fore.GREEN + ". '.  .---.  > " + Fore.MAGENTA + "(_)" + Fore.GREEN + "  )    "
    ligne6 = "|   |" + Fore.MAGENTA + "(_,_)" + Fore.GREEN + "'   '  \\  '-   .''  \\  '-   .'|" + Fore.MAGENTA + "(_" + Fore.GREEN + "    ._) '|  |\\ \\  |  |.'   _    |.---.  \\  : |   | " + Fore.MAGENTA + "(" + Fore.GREEN + "  .  .-'    "
    ligne7 = "|   `-'  /     \\  `-'`   |  \\  `-'`   | |  " + Fore.MAGENTA + "(_" + Fore.GREEN + ".\\.' / |  | \\ `'   /|  _" + Fore.MAGENTA + "( )" + Fore.GREEN + "_  |\\    `-'  | |   |  `-'`-'|___  "
    ligne8 = " \\      /       \\        /   \\        / |       .'  |  |  \\    / \\ " + Fore.MAGENTA + "(_ o _)" + Fore.GREEN + " / \\       /  |   |   |        \\ "
    ligne9 = "  `-..-'         `'-...-'     `'-...-'  '-----'`    ''-'   `'-'   '." + Fore.MAGENTA + "(_,_)" + Fore.GREEN + ".'   `-...-'   '---'   `--------` "
    
    print(Fore.GREEN)
    print(ligne1)
    print(ligne2)
    print(ligne3)
    print(ligne4)
    print(ligne5)
    print(ligne6)
    print(ligne7)
    print(ligne8)
    print(ligne9)
    print(Fore.MAGENTA + "\n                        YGGDRASIL - By https://github.com/0x94sd aka Keryan" + Style.RESET_ALL + "\n")

# [1] Créer/Réinitialiser la base de données

def creer_base_donnees():

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_database
    )

    cursor = conn.cursor()

    
    cursor.execute("DROP TABLE IF EXISTS credentials") # supprime la table credentials si elle existe déjà

    
    cursor.execute("""CREATE TABLE credentials(
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )""") # recrée la table avec UNIQUE sur email

    print("Table credentials recréée avec succès !")

    conn.commit()
    cursor.close()
    conn.close()

# [2] Importer des fichiers .txt

def importer_fichiers():

    dossier = dossier_import

    conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_database
    )

    cursor = conn.cursor() # curseur pour exécuter des commandes SQL


    compteur_fichier = 0
    cred_trop_longues = 0
    cred_trop_longues_fichier = 0

    stats_fichiers = {}

    fichiers_txt = [f for f in os.listdir(dossier) if f.endswith(".txt")]
    nb_fichiers = len(fichiers_txt)

    for fichier in fichiers_txt:
            compteur_fichier += 1
            cred_trop_longues_fichier = 0
            print(f"[{compteur_fichier}/{nb_fichiers}] : {fichier}") # affiche le nom du fichier en cours de traitement et le nombre total de fichiers à traiter
            chemin_complet = os.path.join(dossier, fichier)
            with open(chemin_complet, encoding="UTF-8") as f: 
                    for ligne in f:
                        if ":" in ligne:
                            parties = ligne.split(":")
                            email = parties[0]
                            password = parties[1]
                            if "@" in email:
                                if len(email) <= 255: # vérifie que l'email ne dépasse pas 255 caractères
                                    if len(password) <= 255:
                                        cursor.execute("INSERT INTO credentials (email, password) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING", (email, password))
                                    else:
                                        cred_trop_longues += 1
                                        cred_trop_longues_fichier += 1
            stats_fichiers[fichier] = cred_trop_longues_fichier
    print(f"il y a {cred_trop_longues} identifiants plus longs que 255 caractères dans {fichier}.")

    conn.commit() # applique les changements à la base de données
    cursor.close()
    conn.close()

    # Affichage du tableau récapitulatif
    print("\n" + "="*80)
    print("RÉCAPITULATIF DES LIGNES IGNORÉES (>255 caractères)")
    print("="*80)

    for fichier, nb_ignores in stats_fichiers.items():
        print(f"{fichier:<50} : {nb_ignores:>5} lignes ignorées")

    print("="*80)
    print(f"{'TOTAL GLOBAL':<50} : {cred_trop_longues:>5} lignes ignorées")
    print("="*80)

# [3] Rechercher un email

def rechercher_email():

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_database
    )

    cursor = conn.cursor() # curseur pour exécuter des commandes SQL

    email = input("\nEntre l'email à rechercher: ")
    print()

    cursor.execute("SELECT email, password FROM credentials WHERE email = %s", (email,))

    result = cursor.fetchone() # récupère le premier résultat de la requête SQL, qui contient l'email et le mot de passe correspondant à l'email recherché
    if result != None:
        print(Fore.GREEN + "[+]" + Style.RESET_ALL + f" Email: {result[0]} | " + Fore.GREEN + "[+]" + Style.RESET_ALL + f" Mot de passe: {result[1]}")
    else:
        print(Fore.RED + "[✗]" + Style.RESET_ALL + " Aucun résultat trouvé pour cet email.")

    print(Fore.GREEN + "─" * 50 + Style.RESET_ALL)
    input(Fore.MAGENTA + "⏎ Appuyez sur Entrée pour continuer..." + Style.RESET_ALL)

    
    cursor.close()
    conn.close()

# Choix de l'utilisateur dans le menu principal

while True:
    
    clear_screen()
    
    afficher_logo()

    print(Fore.GREEN + "[1]" + Style.RESET_ALL + " Créer/Réinitialiser la base de données")
    print(Fore.GREEN + "[2]" + Style.RESET_ALL + " Importer des fichiers .txt")
    print(Fore.GREEN + "[3]" + Style.RESET_ALL + " Rechercher un email")
    print(Fore.GREEN + "[4]" + Style.RESET_ALL + " Quitter\n")


    choix = input("Votre choix : ")
    
    if choix == "1":
        print("\nEst-ce que vous êtes sûr de vouloir créer/réinitialiser la base de données ? Cela supprimera toutes les données existantes.\n\n(oui/non)\n")
        confirmation = input("Votre confirmation : ")
        if confirmation.lower() == "oui":
            creer_base_donnees()
        else:
            print("Action annulée. La base de données n'a pas été modifiée.")
    elif choix == "2":
        importer_fichiers()
    elif choix == "3":
        rechercher_email()
    elif choix == "4":
        print(Fore.GREEN + "[4]" + Style.RESET_ALL + " Quitter")
        break