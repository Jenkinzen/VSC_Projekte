from pathlib import Path
import rezeptliste_services as service
from rezeptliste_repository import JsonRezeptRepository




def eingabezahl_pruefen(prompt,min_value=None,max_value=None):
    while True:
        raw = input(prompt)
        try:
            value = int(raw)

        except ValueError:
            print("Bitte eine Zahl eingeben.")
            continue

        if min_value is not None and value < min_value:
            print("Die Nummer ist zu klein.")
            continue

        if max_value is not None and value > max_value:
            print("Die Nummer ist zu groß.")
            continue

        return value

def filter_auswaehlen():
    return eingabezahl_pruefen("Nach welchen Kriterien soll die\n"
                "Rezeptauswahl gefiltert werden?\n\n"
                 "1-[Gerichte]\n"
                 "2-[Zutaten]\n"
                 "3-[Gang]\n\n"
                 "0-[Zurück]:\n\n"
                 "Auswahl:", 
                 min_value=0,
                 max_value=3)


###### ANZEIGE - MENÜ - FUNKTIONEN ################################################################################################################################################################

def show_recipe_by_course(repo):
    while True:
        gang_map = {1: "vorspeise",2: "hauptspeise",3:"dessert"}
        gangeingabe = eingabezahl_pruefen("Welchen Gang möchten Sie wählen?\n\n"
        "1-[Vorspeise],\n"
        "2-[Hauptspeise]\n"
        "3-[Dessert]\n\n" 
        "0-[Zurück]:\n\n"
        "Auswahl:",
        min_value=0, 
        max_value=3)
        
        if gangeingabe == 0:
            return

        gangeingabe = gang_map[gangeingabe]      #wandelt gangeingabe (1,2,3) durch key-value paare die in gang_map oben festgelegt sind in den Gang Namen um(vorspeise,hauptspeise,dessert) 
                                                 # ->heißt mapping, kommt wahrscheinlich durch die "HashMaps" bei Java so, oder beide heißen so wegen irgendwas früherem.
                                                 #habs gegooglet -> to map = zuordnen oder verknüpfen 

        
        

        rezepte = service.filter_recipe_by_course(repo,gangeingabe)
        print()
        for i, rezept in enumerate(rezepte, start=1):
            print(f"{i}. {rezept.name}")

        print()
        print("0-[Zurück]\n")
        while True:
            try:
                nummer = eingabezahl_pruefen("Nummer wählen:\n" 
                ,min_value=0,max_value=len(rezepte))

                if nummer == 0:
                    break

                rezept = service.recipe_by_index(rezepte, nummer)

                if rezept is None:
                    print("Ungültige Nummer.")
                    continue

                for zeile in rezept.anzeigen():
                    print(zeile)

                break

            except ValueError:
                print("Bitte eine Zahl eingeben.")

def show_recipe_by_ingredient(repo):
    while True:
        zutat = [z.strip() for z in input("Welche Zutat(en) möchten Sie wählen?\nBitte Zutaten mit  \",\"  trennen.\n\n" 
        "0-[Zurück]\n").strip().lower().split(",")]

        if zutat == ["0"]:
            return
        
        rezepte = service.filter_recipe_by_ingredient(repo,zutat)

        

        if not rezepte :
            print("Keine Rezepte gefunden.")
            continue    

        for i, rezept in enumerate(rezepte, start=1):
            print(f"{i}. {rezept.name}")

        while True:

            try:
                nummer = eingabezahl_pruefen("Nummer wählen:\n",min_value=0,max_value=len(rezepte))
                rezept = service.recipe_by_index(rezepte, nummer)

                if rezept is None:
                    print("Ungültige Nummer.")
                    continue

                for zeile in rezept.anzeigen():
                    print(zeile)
                    #wenn hier break stehen würde bricht er print(zeile) 
                    #nach der ersten zeile ab ( also printet nur namen aber nicht zutaten,zubereitung etc.)
                break    

            except ValueError:
                print("Bitte eine Zahl eingeben.")  
                #hier brauch man kein continue weil die Schleife hier eh endet und dann wieder anfängt
            
def show_recipe_by_name(repo):
    while True:
        print()
        for i, rezept in enumerate(service.all_recipes(repo), start=1):
            print(f"{i}. {rezept.name}")
        gerichte = service.filter_recipe_by_name(repo,"")
        nummer = eingabezahl_pruefen("\nWählen sie bitte die Nummer des Gerichtes,\n"
        "geben sie 0 ein um zurück zur Kriterienauswahl zu gelangen:\n",min_value=0,max_value=len(gerichte))

        if nummer == 0:
            return

        if nummer > len(gerichte):
            print("Falsche Zahl eingegeben!")
            continue
        rezepte = service.recipe_by_index(gerichte,nummer)

        if not rezepte or 0:
            print("Kein Rezept passt zu diesen Angaben.")
            continue

        
        for zeile in rezepte.anzeigen():
            print(zeile)

def rezepte_ansehen(repo):
    while True:
        filterwahl = filter_auswaehlen()

        if filterwahl == 0:
            return
        
        elif filterwahl == 1:
            show_recipe_by_name(repo)
            continue

        elif filterwahl == 2:
            show_recipe_by_ingredient(repo)
            continue
        
        elif filterwahl == 3:
            show_recipe_by_course(repo)
            continue
        
        
        else:
            print("Ungültige Auswahl.")



####### SPEICHERVERWALTUNGS - MENÜ - FUNKTIONEN ###################################################################################################################################################

def create_recipe(repo):
    rezeptname = input("Wie heißt das Rezept?\n\n" \
    "0-[Zurück]\n\n"
    "Eingabe:").strip()

    if rezeptname == "0":
        return

    zutaten_input = input("Welche Zutaten in welcher Menge brauch es?( Zutaten bitte mit , trennen[z.B. Enokis 200 g, Salz 2 Prise])")
    zutaten_strings = [z.strip() for z in zutaten_input.split(",")if z.strip()]
    zubereitung = input("Wie wird es zubereitet?") 
    notizen = input("Notizen oder Tipps")
    gangeingabe = None
    while gangeingabe is None:
        eingabe = input("Ist es Vorspeise, Hauptspeise oder Dessert? ").strip().lower()
        if service.check_course(eingabe):
                gangeingabe = eingabe
        else:
            print("Ungültige Auswahl! Bitte erneut eingeben.") 

    

    rezept_daten = ({"name":rezeptname,
                         "zutaten":zutaten_strings,
                         "zubereitung":zubereitung,
                         "notizen":notizen,
                         "gang":gangeingabe})

    rezept = service.create_recipe(repo,rezept_daten)
    print(f"{rezept.name} wurde eingefügt!")
    return

def delete_recipe(repo):
        for i, rezept in enumerate(service.all_recipes(repo), start=1):
            print(f"{i}. {rezept.name}")
        
        while True:
            
            gerichte = service.all_recipes(repo)
            nummer = eingabezahl_pruefen("Welche Nummer soll gelöscht werden?\n"
            "0-[Zurück]:\n",min_value=0,max_value=len(gerichte))                # len(alle_rezepte())würde auch gehen aber so ist es effizienter und logischer wenn
                                                                                # schon durch gerichte einmal die funktion aufgerufen wurde.
            if nummer == 0:
                break
            
            rezept_zum_loeschen = service.recipe_by_index(gerichte,nummer)

            if rezept_zum_loeschen is None:
                print("Rezept nicht gefunden.")
                return

            for zeile in rezept_zum_loeschen.anzeigen():
                print(zeile)
                
            rueckversichern = input(f"Sind sie sicher, dass {rezept_zum_loeschen.name} gelöscht werden soll? Ja/Nein").strip().lower()

            if rueckversichern.strip().lower() == "ja":
                    service.delete_recipe(repo,rezept_zum_loeschen.name)
                    print(f"{rezept_zum_loeschen} wurde gelöscht!")
                    return
            
            else:
                print(f"{rezept_zum_loeschen} wird nicht gelöscht.")
                break

def update_recipe(repo):
    rezeptname = input("Welches Gericht soll geupdatet werden?")
    if service.check_recipename(repo,rezeptname):
        rezeptoderzutatattribut = input("Möchten sie etwas im Rezept oder etwas in der Zutatenliste ändern?('zutat' oder 'rezept' eingeben)")
        if rezeptoderzutatattribut == "zutat":
            zutatauswahl = input("Welche Zutat möchten sie ändern?")
            if service.check_ingredient_in_recipe(repo,rezeptname,zutatauswahl):
                attributauswahl = input("Was möchten sie ändern?")
                if service.check_ingredient_attribute(repo,rezeptname,zutatauswahl,attributauswahl):
                    aenderungsauswahl = input("Neuer Eintrag: ")
                    service.update_recipe(repo,rezeptname,aenderungsauswahl,"zutaten",zutatauswahl,attributauswahl)
                    print("Eintrag wurde geändert.")

        elif rezeptoderzutatattribut == "rezept":
            attributauswahl = input("Was möchten sie ändern?")
            if service.check_attribute(repo,rezeptname,attributauswahl):
                aenderungsauswahl = input("Neuer Eintrag: ")
                service.update_recipe(repo,rezeptname,aenderungsauswahl,attributauswahl)
        else:
            print("Ungültige Auswahl!")
            return
    else:
        print("Ungültiger Rezeptname!")
        return


#(repo: JsonRezeptRepository, gesuchtesrezept: str,aenderung:str,rezeptattribut:str,gesuchtezutat:str|None = None,zutatenattribut:str| None = None )


