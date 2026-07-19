import rezeptliste_ui as ui
from pathlib import Path
import rezeptliste_services as service
from rezeptliste_repository import JsonRezeptRepository 
from rezeptliste_repository import SqlRezeptRepository
import fastapi
from typing import List
import rezeptliste_model as model
import rezeptliste_schemas as schemas
app = fastapi.FastAPI()  #erstellt API Anwendung


BASE_DIR = Path(__file__).resolve().parent

DB_DATEI = BASE_DIR / "databases" / "rezepte.db"

DATEI = BASE_DIR / "databases" / "rezepte.json" #link zum speicherort der json Datei





REPOSITORY_TYP = "sql"              # hier zwischen json und sql repo wechseln

if REPOSITORY_TYP == "json":
    repo = JsonRezeptRepository(DATEI)   
    repo.load()

elif REPOSITORY_TYP =="sql":
    repo = SqlRezeptRepository(DB_DATEI)

else:
    raise ValueError("Unbekannter Repository-Typ")



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

@app.get("/rezepte",status_code=200,response_model=list[schemas.RecipeResponse])
def find_all_recipes():
    return repo.all()
    

@app.get("/rezepte/suchen",status_code=200,response_model=list[schemas.RecipeResponse])
def search_recipes(
    name: str | None = None,
    gang: str | None = None,
    match: str = fastapi.Query(default="any"),
    zutaten: List[str] = fastapi.Query(default=[])):

    match = match.strip().lower()

    if match == "all":
        all_match_recipe = service.match_all_search_recipes(repo,name,gang,zutaten)
        
        if not all_match_recipe:
            raise fastapi.HTTPException(status_code=404, detail="Kein passendes Rezept gefunden")

        return all_match_recipe

    elif match == "any":
        any_match_recipe = service.match_any_search_recipes(repo,name,gang,zutaten)

        if not any_match_recipe:
            raise fastapi.HTTPException(status_code=404, detail="Kein passendes Rezept gefunden")
        
        return any_match_recipe
    
    else:
        raise fastapi.HTTPException(status_code=400,detail="match muss any oder all sein")
    
    
    

@app.get("/rezepte/exakt/{sucheingabe}", status_code=200,response_model=schemas.RecipeResponse)
def find_recipe_endpoint(recipe_id: int):
    recipe = service.find_exact_recipe(repo, recipe_id)                 # repo -> yo hier ist mein repo, service.rezept_finden sucht dir raus was du brauchst und ich übergeb es dir dann!

    if recipe is None:
        raise fastapi.HTTPException(status_code=404, detail="Rezept nicht gefunden")
    
    return recipe
    

@app.post("/rezepte/speicher/erstellen", status_code=201,response_model=schemas.RecipeResponse)
def create_recipe_endpoint(rezept_daten: schemas.RecipeCreate):      #rezept_daten ist die variable für die eingegebenen Daten des neu zu erstellenden Rezeptes 
    createdrecipe = service.create_recipe(repo,rezept_daten)

    if createdrecipe is None:
        raise fastapi.HTTPException(status_code=400, detail="Rezept konnte nicht erstellt werden")
    
    return createdrecipe

@app.delete("/rezepte/speicher/löschen/{rezeptname}", status_code=200,response_model=schemas.MessageResponse)
def delete_recipe_endpoint(rezept_id: int):
    deletedrecipe = service.delete_recipe(repo,rezept_id)

    if not deletedrecipe:           # is None ist hier fehleranfällig weil die delete_recipe funktion nur True oder False zurückgibt und kein erstelltes rezept oder ein gesuchtes rezept
        raise fastapi.HTTPException(status_code=404, detail="Löschung ist fehlgeschlagen!")
    
    return {"info":"Rezept wurde gelöscht!"}

@app.patch("/rezepte/speicher/multiupdate",status_code=200,response_model=schemas.MessageResponse)
def multi_update_recipe_endpoint(rezept_daten: schemas.MultiUpdateCreate):
    updatedrecipe = service.multi_update_recipe(repo,rezept_daten)

    if not updatedrecipe:
        raise fastapi.HTTPException(status_code=404, detail="Update fehlgeschlagen.")

    
    return {"info":"Update erfolgreich!"}
    


