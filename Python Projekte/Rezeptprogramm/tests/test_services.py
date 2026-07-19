import pytest
import rezeptliste_services as service
import rezeptliste_model as model
import rezeptliste_schemas as schemas
from rezeptliste_repository import JsonRezeptRepository


"""Damit pytest Sachen findet , Ordner immer mit test_[irgendwas].py oder [irgendwas]_test.py betiteln
und auch test funktionen immer mit test_ beginnen damit pytest diese automatisch im ordner findet."""

"""Genereller Testaufbau:
    Arrange - Daten aufbauen (hier wird ja über den monkeypatch ne leere Liste aufgerufen, also muss man ein Rezept im Test einfügen um an diesem Rezept zu testen [zumindest mit monkeypatch])
    Act     - Funktion aufrufen(Die funktion die man halt testen möchte)
    Assert  - per assert funktion die Erwartungen überprüfen die man hat[ (assert service.gang_pruefen("Dessert") is True ) ] bspw.

    /to assert - behaupten | -> ich behaupte dies und das wird dabei raus kommen, stimmt das?
    """

@pytest.fixture
def repo(tmp_path):
    datei = tmp_path / "rezepte.json"
    r = JsonRezeptRepository(datei)
    r.load()  # startet leer, weil Datei noch nicht existiert
    return r
    



def test_rezept_finden_case_insensitive(repo):
    repo.add(model.Rezept("Spaghetti", [], "z", "Hauptspeise", ""))

    result = service.find_exact_recipe(repo,1)
    assert result is not None
    assert result.name == "Spaghetti"

    assert service.find_exact_recipe(repo,400) is None

def test_filter_rezepte_nach_gang(repo):
    repo.add(model.Rezept("A", [], "z", "Dessert", ""))
    repo.add(model.Rezept("B", [], "z", "Hauptspeise", ""))

    result = service.match_all_search_recipes(repo,None,"hauptspeise",None)
    assert [r.name for r in result] == ["B"]

def test_filter_rezepte_nach_zutaten_all_must_match(repo):
    repo.add(model.Rezept(
        "Pasta",
        [model.Zutaten("tomate", None, "stück"), model.Zutaten("salz", None, "prise")],
            "z",
            "Hauptspeise",
        ""
    ))
    repo.add(model.Rezept(
        "Brot",
        [model.Zutaten("mehl", "500", "g"), model.Zutaten("salz", None, "prise")],
        "z",
        "Hauptspeise",
        ""
    ))
    result = service.match_any_search_recipes(repo,None,None,["salz", "tomate"])
    assert ["Pasta","Brot"] == [r.name for r in result]  



def test_gang_pruefen(repo):

    repo.add(model.Rezept("Irgendwas leckeres",[model.Zutaten("Schweinekopf",None,None,None)
                                                ,model.Zutaten("Krähenfüße",None,None,None)
                                                ,model.Zutaten("Handwaschlappen",None,None,None)]
                                                ,"Einfach roh essen","hauptspeiße","grrrr"))
     
    test1 = service.match_all_search_recipes(repo,None,"hauptspeiße",None)
    test2 = service.match_all_search_recipes(repo,None,"hauptspeiße",None)
    test3 = service.match_all_search_recipes(repo,None," hauptspeiße ",None)
    
    assert [rezept.name for rezept in test1] == ["Irgendwas leckeres"]
    assert [rezept.gang for rezept in test2] == ["hauptspeiße"]
    assert "Schweinekopf" in [alle_zutaten.name for rezept in test3 for alle_zutaten  in rezept.zutaten] 
    
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

def test_filter_rezepte_nach_gericht(repo):

    repo.add(model.Rezept("Kokoscurry-Sushibowl-Schokomousse",[],"x","x","x"))
    repo.add(model.Rezept("Misosuppe",[],"x","x","x"))

    #wahr

    result1 = service.match_any_search_recipes(repo,"Curr",None,None) 
    result2 = service.match_any_search_recipes(repo,"sUsH ",None,None) 
    result3 = service.match_any_search_recipes(repo," schok",None,None) 
    result4 = service.match_any_search_recipes(repo,"Miso",None,None)
    result5 = service.match_any_search_recipes(repo,"su",None,None)

    assert any(r.name for r in result1) 
    assert (r.name == "Kokoscurry-Sushibowl-Schokomousse" for r in result2) 
    assert any(r.name for r in result3)
    assert (r.name == "Misosuppe" for r in result4)
    assert {r.name  for r in result5} == {"Kokoscurry-Sushibowl-Schokomousse","Misosuppe"}

    """Testet durch {} generell ob die beiden Namen, und NUR die beiden Namen im Set(so heißt das wenn man
    ne Liste mit {} einklammert) sind. Die Reihenfolge ist egal.
     Wenn diese beiden im Set enthalten sind, aber noch irgendetwas anderes dadrin wäre der test falsch."""
    
    assert [r.name  for r in result5] == ["Kokoscurry-Sushibowl-Schokomousse","Misosuppe"]

    """Testet durch [] als Liste, der unterschied ist, hier muss die Reihenfolge stimmen( by default ist
    die Reihenfolge > was als erstes eingefügt wurde kommt zuerst dran[also hier erst kokosbla dann Misosuppe])
    deshalb """


    """WICHTIG!!!! WENN MAN EIN SET {} TESTET MUSS AUCH DIE LC EIN SET{} SEIN.
                   WENN MAN EINE LIST [] TESTET MUSS AUCH DIE LC EINE LIST [] SEIN. """
    
    """ ALTERNATIV KANN MAN EINE LISTE WIE UNTEN IN DER OPTIMIERTEN VERSION ZUM SET 
                    UMWANDELN:
                    assert set(names("e")) == {"Kokoscurry-Sushibowl-Schokomousse","Ekelpampe"}"""
    

    assert any(r.name for r in service.match_any_search_recipes(repo,"Curr"))

    #falsch

    result4 = service.match_any_search_recipes(repo,"myv2",None,None)  
    result5 = service.match_any_search_recipes(repo,"ölgi",None,None)   
    result6 = service.match_any_search_recipes(repo,"3425",None,None) 

    assert not any(r.name for r in result5) 
    assert not any(r.name for r in result6)
    assert not any(r.name for r in result4) 
    assert not [r.name  for r in result5] == ["Misosuppe","Kokoscurry-Sushibowl-Schokomousse"]

def test_filter_rezepte_nach_gericht_optimal(repo):

    repo.add(model.Rezept("Kokoscurry-Sushibowl-Schokomousse",[],"x","x","x"))

    #wahr

    assert any(r.name for r in service.match_any_search_recipes(repo,"Curr",None,None))
    assert any(r.name for r in service.match_any_search_recipes(repo,"sUsH",None,None))
    assert any(r.name for r in service.match_any_search_recipes(repo," schok",None,None))

    #falsch

    assert not any(r.name for r in service.match_any_search_recipes(repo,"g932d",None,None))
    assert not any(r.name for r in service.match_any_search_recipes(repo,"schnokomabe",None,None))
    assert not any(r.name for r in service.match_any_search_recipes(repo,"miep-2xx.r9",None,None))   
"""Optimierung von GPT"""
def test_filter_rezepte_nach_gericht_noch_krasser_optimiert(repo):


    repo.add(model.Rezept("Kokoscurry-Sushibowl-Schokomousse", [], "x", "x", "x"))
    repo.add(model.Rezept("Ekelpampe",[],"x","x","x"))
                            
    def names(repo,q):
        return [r.name for r in service.match_any_search_recipes(repo,q)]

    # wahr (Teilstrings + case + whitespace)
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(repo,"Curr")
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(repo,"sUsH ")
    assert "Kokoscurry-Sushibowl-Schokomousse" in names(repo," schok")

    assert set(names(repo,"e")) == {"Kokoscurry-Sushibowl-Schokomousse","Ekelpampe"}

    # falsch
    assert names(repo,"g932d") == []
    assert names(repo,"schnokomabe") == []
    assert names(repo,"miep-2xx.r9") == []
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
def test_alle_rezepte(repo):

    repo.add(model.Rezept("1",[],"x","x","x"))
    repo.add(model.Rezept("2",[],"x","x","x"))
    repo.add(model.Rezept("3",[],"x","x","x"))
    repo.add(model.Rezept("4",[],"x","x","x"))
    repo.add(model.Rezept("5",[],"x","x","x"))
    repo.add(model.Rezept("6",[],"x","x","x"))

    def names():
        return len([r.name for r in repo.all()])
    
    assert names() == 6
# wichtig!! nur mit names klappt es nicht, die () is wichtig und heißt "führe diese funktion jetzt aus"
"""Optimale Form von Chat GPT """
def test_alle_rezepte_optimal(repo):

    repo.add(model.Rezept("1",[],"x","x","x"))
    repo.add(model.Rezept("2",[],"x","x","x"))
    repo.add(model.Rezept("3",[],"x","x","x"))
    repo.add(model.Rezept("4",[],"x","x","x"))
    repo.add(model.Rezept("5",[],"x","x","x"))
    repo.add(model.Rezept("6",[],"x","x","x"))

    assert len(repo.all()) == 6
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
def test_rezept_loeschen(repo):
    repo.add(model.Rezept("Handfeuerwaffeln",[],"x","x","x"))

    rezept = service.match_all_search_recipes(repo,"Handfeuerwaffeln",None,None)
    assert rezept is not None
    service.delete_recipe(repo,1) 
    assert len(repo.all()) == 0  
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""
def test_rezept_einfuegen(repo):
    
    recipe_data=schemas.RecipeCreate(name="Handfeuerwaffeln",zutaten=[schemas.IngredientCreate(zutatenname="Waffeln",menge="4" ,einheit="Stück"),
                                                                schemas.IngredientCreate(zutatenname="Schießpulver",menge="200",einheit="g"),
                                                                schemas.IngredientCreate(zutatenname="Schnittlauch",menge=None,einheit="Bündel"),],
                                                                zubereitung="x",
                                                                gang="x",
                                                                notizen="x")
    
    service.create_recipe(repo,recipe_data)

    assert len(repo.all()) == 1

    rezept = repo.all()[0]

    schnittlauch = next(z for z in rezept.zutaten if z.name == "Schnittlauch")
    schießpulver = next(z for z in rezept.zutaten if z.name == "Schießpulver")
    waffeln = next(z for z in rezept.zutaten if z.name == "Waffeln")

    assert schnittlauch.menge is None
    assert schnittlauch.einheit == "Bündel"
    assert waffeln.einheit == "Stück"
    assert schießpulver.menge == "200"

    assert waffeln.menge != "5"
    assert schießpulver.name != "piesschulver"
    assert schnittlauch.menge != "12" 
"""xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"""

