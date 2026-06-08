from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# python -m pytest tests/test_api.py -v    COMMANDBEFEHL FÜR API TEST
# [python ruft -m(odul) pytest auf | -> tests/test_api.py Pfad dieser Datei | -v = zeigt ob die tests erfolgreich waren, mit -s dahinter zeigt es auch noch die prints der responses]
def test_find_all_recipes():
    response = client.get("/rezepte")

    assert response.status_code == 200
    print(response.json())
    
def test_recipe_by_index():
    response = client.get("/rezepte/2")         # bei sowas einfach suchbegriff ohne {} dran hängen

    assert response.status_code == 200
    print(response.json())

def test_find_recipe_endpoint():
    response = client.get("/rezepte/suche/Schokomousse")

    assert response.status_code == 200
    print(response.json())

def test_filter_recipe_by_name_endpoint():
    response = client.get("/rezepte/filter/gerichte/Sushibowl")

    assert response.status_code == 200
    print(response.json())


#########################################################


def test_delete_recipe_endpoint():
    response = client.delete("/rezepte/speicher/löschen/Schlammsuppe")

    assert response.status_code == 404
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