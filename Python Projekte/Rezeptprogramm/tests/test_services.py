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
    
def test_recipe_create(repo):
    test_recipe_datas = schemas.RecipeCreate(
        name="Test_Rezept", 
        zutaten=[schemas.IngredientCreate(
                  zutatenname="Test_Zutat 1",
                  menge="Test_Menge 1",
                  einheit="Test_Einheit 1"),
                  schemas.IngredientCreate(
                  zutatenname="Test_Zutat 2",
                  menge="Test_Menge 2",
                  einheit="Test_Einheit 2")
                  ],
        zubereitung="Test_Zubereitung",
        gang="hAuPtSpeIße",          
        notizen="Test_Notiz",
    )

    service.create_recipe(repo,test_recipe_datas)

    recipe = service.find_exact_recipe(repo,1)

    assert recipe is not None
    
    assert recipe.name == "Test_Rezept"

def test_recipe_delete(repo):
    test_recipe_datas = schemas.RecipeCreate(
        name="Test_Rezept", 
        zutaten=[schemas.IngredientCreate(
                  zutatenname="Test_Zutat 1",
                  menge="Test_Menge 1",
                  einheit="Test_Einheit 1"),
                  schemas.IngredientCreate(
                  zutatenname="Test_Zutat 2",
                  menge="Test_Menge 2",
                  einheit="Test_Einheit 2")
                  ],
        zubereitung="Test_Zubereitung",
        gang="hAuPtSpeIße",          
        notizen="Test_Notiz",
    )

    service.create_recipe(repo,test_recipe_datas)

    service.delete_recipe(repo,1)
    
def test_find_exact_recipe(repo):
    repo.add(model.Rezept("Spaghetti", [], "z", "Hauptspeise", ""))

    result = service.find_exact_recipe(repo,1)
    assert result is not None
    assert result.name == "Spaghetti"

    assert service.find_exact_recipe(repo,400) is None

def test_find_exact_ingredient(repo):
    repo.add(model.Rezept("Irgendwas leckeres",[model.Zutaten("Schweinekopf",None,None,1)
                                                ,model.Zutaten("Krähenfüße",None,None,2)
                                                ,model.Zutaten("Handwaschlappen",None,None,3)]
                                                ,"Einfach roh essen","hauptspeiße","grrrr",1))

    
    searched_recipe = service.find_exact_recipe(repo,1)

    assert searched_recipe is not None

    searched_ingredient = service.find_exact_ingredient(searched_recipe,1)

    assert searched_ingredient is not None

    assert searched_ingredient.name == "Schweinekopf"

def test_match_all_search_recipes(repo):
    repo.add(model.Rezept("A", [], "z", "Dessert", ""))
    repo.add(model.Rezept("B", [], "z", "Hauptspeise", ""))

    result = service.match_all_search_recipes(repo,None,"hauptspeise",None)
    assert [r.name for r in result] == ["B"]
    assert [r.name for r in result] != ["A"]
        
def test_match_any_search_recipes(repo):
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
    assert "tomate" and "salz" in [z.name for r in result for z in r.zutaten]
    assert "gramm" not in [attribut.einheit for recipe in result for attribut in recipe.zutaten]
    assert len(result) == 2

def test_update_recipe(repo):
    repo.add(model.Rezept("Test_Rezept 2",
                          [model.Zutaten("Test_Zutat 3",
                                        "Test_Menge 3",
                                        "Test_Einheit 3",
                                        1,
                                        None),
                                        model.Zutaten("Test_Zutat 4",
                                        "Test_Menge 4",
                                        "Test_Einheit 4",
                                        2,
                                        None)],                                          
                                        "Test_Zubereitung 2",
                                        "vorspeiße",
                                        "",
                                        2))
    
    updated_recipe = schemas.RecipeUpdate(aenderung="rezept",rezept_id=1,zutat_id=None,name_neu=None,zutaten=[],zubereitung_neu=None,gang_neu="hauptspeiße",notizen_neu=None)

    service.update_recipe(repo,updated_recipe)

    test_recipe = service.find_exact_recipe(repo,1)

    assert test_recipe is not None

    assert "hauptspeiße" == test_recipe.gang

    

def test_workflow(repo):
    test_recipe_datas = schemas.RecipeCreate(
        name="Test_Rezept 1", 
        zutaten=[schemas.IngredientCreate(
                  zutatenname="Test_Zutat 1",
                  menge="Test_Menge 1",
                  einheit="Test_Einheit 1"),
                  schemas.IngredientCreate(
                  zutatenname="Test_Zutat 2",
                  menge="Test_Menge 2",
                  einheit="Test_Einheit 2")
                  ],
        zubereitung="Test_Zubereitung 1",
        gang="hAuPtSpeIße 1",          
        notizen="Test_Notiz 1",
    )

    service.create_recipe(repo,test_recipe_datas)

    result = service.find_exact_recipe(repo,1)

    repo.add(model.Rezept("Test_Rezept 2",
                          [model.Zutaten("Test_Zutat 3",
                                        "Test_Menge 3",
                                        "Test_Einheit 3",
                                        1,
                                        None),
                                        model.Zutaten("Test_Zutat 4",
                                        "Test_Menge 4",
                                        "Test_Einheit 4",
                                        2,
                                        None)],                                          
                                        "Test_Zubereitung 2",
                                        "vorspeiße",
                                        "",
                                        2))
    
    repo.add(result)

    assert result is not None

    assert "Test_Rezept 1" ==  result.name

    updated_recipe = schemas.RecipeUpdate(aenderung="rezept",rezept_id=1,zutat_id=None,name_neu=None,zutaten=[],zubereitung_neu=None,gang_neu="hauptspeiße",notizen_neu=None)

    service.update_recipe(repo,updated_recipe)

    assert "hauptspeiße 1" == result.gang.lower().strip()

    find_recipe_2 = service.find_exact_recipe(repo,2)

    assert find_recipe_2 is not None

    assert find_recipe_2.name == "Test_Rezept 2"

    ingredient_result = service.find_exact_ingredient(find_recipe_2,1)

    assert ingredient_result is not None

    assert ingredient_result.name == "Test_Zutat 3"

    



