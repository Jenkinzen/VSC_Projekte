from fastapi.testclient import TestClient
import rezeptliste_api 
from pathlib import Path
from rezeptliste_repository import SqlRezeptRepository
from rezeptliste_repository import JsonRezeptRepository


client = TestClient(rezeptliste_api.app)

TEST_BASE_DIR = Path(__file__).resolve().parent

TEST_DB_DATEI = TEST_BASE_DIR / "test_databases" / "rezepte_api_test.db"
TEST_JSON_DATEI = TEST_BASE_DIR / "rezepte_api_test.json"


switch = "sql"

if switch == "sql":
    test_repo = SqlRezeptRepository(TEST_DB_DATEI)
    rezeptliste_api.repo = test_repo
if switch == "json":
    test_repo =  JsonRezeptRepository(TEST_JSON_DATEI)
    rezeptliste_api.repo = test_repo



# python -m pytest tests/test_api.py -v    COMMANDBEFEHL FÜR API TEST
# [python ruft -m(odul) pytest auf | -> tests/test_api.py Pfad dieser Datei | -v = zeigt ob die tests erfolgreich waren, mit -s dahinter zeigt es auch noch die prints der responses]
def create_recipe():
    response = client.("/rezepte/speicher/erstellen")

def test_find_all_recipes():
    response = client.get("/rezepte")

    assert response.status_code == 200
    print(response.status_code)
    print(response.json())
    

def test_find_recipe_by_name_endpoint():
    response = client.get("/rezepte/suchen/",params={"name":"KAFFEEEEEEEEE"})


    assert response.status_code == 200
    print(response.status_code)
    print(response.json())

def test_find_recipe_by_course_endpoint():
    response = client.get("/rezepte/suchen/",params={"gang":"hauptspeiße"})


    assert response.status_code == 200
    print(response.status_code)
    print(response.json())

def test_find_recipe_by_ingredient_endpoint():
    response = client.get("/rezepte/suchen/",params={"zutaten":["Kaffeepulver"]})   #zutaten : ist ein query parameter, er sucht an dieser stelle jeden string der zutaten durch deshalb muss man nicht "name":"Kaffeepulver" schreiben, so kann sogar eine einheit gesucht werden oder die menge weil er in allen strings innerhalb der Liste zutaten sucht


    assert response.status_code == 200
    print(response.status_code)
    print(response.json())


def test_delete_recipe_endpoint():
    response = client.delete("/rezepte/speicher/löschen/Schlammsuppe")

    assert response.status_code == 404
    print(response.status_code) 
    print(response.json())








#CODE CHEAT SHEET
"""
200 OK		                Daten erfolgreich abgerufen
201 Created		            POST legt neues Rezept an
204 No Content		        DELETE erfolgreich
400 Bad Request	            Anfrage fehlerhaft	Falsche Parameter, ungültige Eingaben
401 Unauthorized	        Login fehlt oder Token fehlt
403 Forbidden	            keine Berechtigung	Benutzer darf Aktion nicht ausführen
404 Not Found	            Ressource nicht gefunden	Rezept existiert nicht
409 Conflict	            Konflikt mit bestehendem Zustand	Rezeptname existiert bereits
422 Unprocessable Content	Anfrage formal korrekt, Inhalt ungültig	FastAPI/Pydantic-Validierungsfehler
500 Internal Server Error	Fehler auf dem Server	Unbehandelte Exception im Code
"""