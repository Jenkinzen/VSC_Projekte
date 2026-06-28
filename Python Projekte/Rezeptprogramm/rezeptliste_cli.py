import rezeptliste_ui as ui
from pathlib import Path
import rezeptliste_services as service
from rezeptliste_repository import JsonRezeptRepository
import rezeptliste_model as model
import rezeptliste_api as api

def cli_starten():
    neustart = True

    while neustart:

        Menueauswahl = input("Möchten sie ein Rezept \n\n"
        "1-[ansehen]\n"
        "2-[ändern]\n"
        "3-[einfügen]\n"
        "4-[löschen]\n"
        "0-[exit]\n\n"
        "Eingabe:")



        if Menueauswahl == "1":

            ui.rezepte_ansehen(api.repo)


        elif Menueauswahl == "2":

            ui.update_recipe(api.repo)


        elif Menueauswahl == "3":

            ui.create_recipe(api.repo)


        elif Menueauswahl == "4":
            
            ui.delete_recipe(api.repo)


        elif Menueauswahl == "0":
            break  


        else:
            print("Ungültige Auswahl!")
            continue

if __name__ == "__main__":
    cli_starten()
        
