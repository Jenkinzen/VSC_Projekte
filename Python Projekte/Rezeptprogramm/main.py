import rezeptliste_ui as ui
from pathlib import Path
import rezeptliste_services as service
from rezeptliste_repository import JsonRezeptRepository
import fastapi
from typing import List
from fastapi import Query
import rezeptliste_model as model
import rezeptliste_schemas as schemas
app = fastapi.FastAPI()  #erstellt API Anwendung



DATEI = Path(__file__).resolve().parent.parent.parent / "Data"/ "RezeptData"/ "rezepte.json" #link zum speicherort der json Datei

repo = JsonRezeptRepository(DATEI)
repo.load()

"""momentaner Ablauf: JSON Datei auf der Festplatte hat die Rezepte als JSON-Format(sieht exakt aus wie ein dict, ist aber als JSON einfach nur ein text Datentyp der besonders angeordnet wird)
 Durch json.load() wandelt Python es in ein Python dict um... ab dem Punkt nennt man es dann ein dict, da es nun von python zum datentyp dict umgewandelt wurde
 (Schlüssel-Wert-Paare[Attribut-Objekteintrag]). Durch Python wird mithilfe der Anleitung im repository WIE das dict in Objekte umgewandelt werden soll (das nennt man Mapping), 
das dict in Objekte umgewandelt. Bis hierhin plain JSON - Python stuff ohne API. Jetzt mit der API wird ab diesem Punkt dank @dataclass in rezeptliste_model (das quasi als Verweis für die API 
gilt wie die Objektdaten strukturiert werden müssen, damit sie von der API "serialisiert" werden können) da HTTP keine Objekte versteht, muss eine Anleitung genutzt werden die der API sagt wie 
der Inhalt des Objektes "organisiert" wird um eine HTTP und API konforme Datenstruktur aus den Objektinhalten zu machen damit sie von der API genutzt werden kann.
And you guessed it , dieses Datenformat ist wieder JSON. 

Also JSON auf Festplatte -> durch json.load in Python dict -> durch repo-Mapper dict mit Python in Objekt im Repo(Speicher während der Ausführung) -> durch @dataclass Referenz kann die API die 
Objekte wieder in JSON umwandeln und sie somit nutzen. 

Denn JSON ist ein einheitliches Format für den Datentransport. Zwischen Endpunkt und Anwendung , zwischen Programmiersprachen oder Programmen, das 
Format um datenübergreifend von a nach b zu senden ist JSON. Quasi die Europalette der virtuellen Lagerlogistik."""

@app.get("/")       #app.get is standartbefehl um eine URL über API aufzurufen
                    # () parameter in den die jeweilige URL rein kommt
def root():
    return {"message": "Moin Moin meine aktiven Freunde"}

@app.get("/rezepte")
def find_all_recipes():
    return repo.all()



@app.get("/rezepte/{nummer}")
def recipe_by_index_endpoint(nummer: int):
    return service.recipe_by_index(repo.all(), nummer)           # repo.alle() -> yo hier ich übergeb dir das komplette repo! (macht sinn bei der funktion die ALLES im repo anzeigen soll)

@app.get("/rezepte/suche/{sucheingabe}")
def find_recipe_endpoint(sucheingabe: str):
    return service.find_recipe(repo, sucheingabe)                 # repo -> yo hier ist mein repo, service.rezept_finden sucht dir raus was du brauchst und ich übergeb es dir dann!



@app.get("/rezepte/filter/gerichte/{gericht}")
def filter_recipe_by_name_endpoint(gericht: str):
    return service.filter_recipe_by_name(repo,gericht)

@app.get("/rezepte/filter/gang/{gang}")
def filter_recipe_by_course_endpoint(gang: str):
    return service.filter_recipe_by_course(repo,gang)

@app.get("/rezepte/filter/zutaten")                                 # weil es mehrere inputs gibt brauch man hier kein {bla}, das klappt nur mit 1 input. Siehe API -> die regelt das automatisch
def filter_recipe_by_ingredients(zutaten: List[str] = Query()):
    return service.filter_recipe_by_ingredient(repo,zutaten)

#API macht alles, geht so aber SoC konform sollte rezept_erstellen die Buisnesslogik haben und API nur senden.
@app.post("/rezepte/speicher/erstellen")
def create_recipe_endpoint(rezept_daten: schemas.RecipeCreate):      #rezept_daten ist die variable für die eingegebenen Daten des neu zu erstellenden Rezeptes 
    return service.create_recipe(repo,rezept_daten)

@app.delete("/rezepte/speicher/löschen")
def delete_recipe_endpoint(rezeptname: str):
    success = service.delete_recipe(repo,rezeptname)

    if not success:
        raise fastapi.HTTPException(status_code=404, detail="Löschung ist fehlgeschlagen!")
    
    return {"Info":"Rezept wurde gelöscht!"}

@app.patch("/rezepte/speicher/update")
def update_recipe_endpoint(rezept_daten: schemas.UpdateCreate ):
    success = service.update_recipe(repo,rezept_daten)

    if not success:
        raise fastapi.HTTPException(status_code=404, detail="Rezept, Zutat oder Attribut nicht gefunden")

    
    return {"Info":"Update erfolgreich!"}
    


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

            ui.rezepte_ansehen(repo)


        if Menueauswahl == "2":

            ui.update_recipe(repo)


        elif Menueauswahl == "3":

            ui.create_recipe(repo)


        elif Menueauswahl == "4":
            
            ui.delete_recipe(repo)


        elif Menueauswahl == "0":
            break  


        else:
            print("Ungültige Auswahl!")
            continue

if __name__ == "__main__":
    cli_starten()
        
