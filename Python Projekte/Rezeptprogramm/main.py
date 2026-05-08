import rezeptliste_ui as ui
from pathlib import Path
import rezeptliste_services as service
from rezeptliste_repository import JsonRezeptRepository


DATEI = Path(__file__).resolve().parent.parent.parent / "Data"/ "RezeptData"/ "rezepte.json" #link zum speicherort der json Datei

repo = JsonRezeptRepository(DATEI)
repo.load()

neustart = True

while neustart:

    Menueauswahl = input("Möchten sie ein Rezept \n\n"
    "1-[ansehen]\n"
    "2-[einfügen]\n"
    "3-[löschen]\n\n"
    "Eingabe:")



    if Menueauswahl == "1":

        ui.rezepte_ansehen(repo)



    elif Menueauswahl == "2":

        ui.rezept_einfuegen(repo)



    elif Menueauswahl == "3":
        
        ui.rezept_loeschen(repo)
        


    else:
        print("Ungültige Auswahl!")
        continue
        
