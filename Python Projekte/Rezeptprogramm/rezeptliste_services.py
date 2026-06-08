import rezeptliste_model as model
import rezeptliste_storage as storage
from typing import List, Optional
from rezeptliste_repository import JsonRezeptRepository
import rezeptliste_schemas as schemas

#LIST COMP CHEAT SHEET



#result = []                    # wird unten durch [] in der die LC steht ersetzt
#for r in repo.all():           # steht unten einfach hintereinander
#   if r.gang == "Dessert":     # steht unten einfach hintereinander
#       result.append(r.name)   # wird unten durch r.name am Anfang ersetzt

#[WAS for WERT in QUELLE if BEDINGUNG]
#[r.name for r in repo.all() if r.gang == "Dessert"]

######## BASISZUGRIFF - LESEN #################################################################################################################################

 
def all_recipes(repo: JsonRezeptRepository) -> List[model.Rezept]:
    return repo.all()

def recipe_by_index(recipe: List[model.Rezept], index: int) -> Optional[model.Rezept]:
    """index = auswahl der Gerichtnummer im UI.
    wenn die auswahl größer gleich 1 ist und kleiner als die
    gesamtanzahl an rezepten (len(recipe) nummeriert die einzelnen Objekte in der Liste durch
    ,hier halt die Rezepte in der Liste Gerichte)"""
    if 1 <= index <= len(recipe):
        return recipe[index - 1]
    return None

def find_exact_recipe(repo: JsonRezeptRepository, recipename: str) -> Optional[model.Rezept]:

    return repo.find_recipe_by_input(recipename)


######## VALIDIERUNG ##############################################################################################################################################
def check_recipename(repo: JsonRezeptRepository,recipename) -> bool:
    if repo.find_recipe_by_input(recipename):
        return True
    return False

def check_attribute(repo: JsonRezeptRepository,rezeptname,attributname) -> bool:
    if hasattr(find_exact_recipe(repo,rezeptname),attributname) is not None:
        return True
    return False

def check_ingredient_attribute(repo: JsonRezeptRepository,recipename,ingredientname,attributename) -> bool:
    if hasattr(repo.find_ingredient_in_one_recipe(recipename,ingredientname),attributename) is not None:
        return True
    return False

def check_ingredient_in_recipe(repo: JsonRezeptRepository,recipename,ingredientname) -> bool:
    if repo.find_ingredient_in_one_recipe(recipename,ingredientname)is not None:
        return True
    return False

def check_course(courseinput):
    return courseinput.lower().strip() in storage.GUELTIGE_GAENGE

def validate_course(recipes, courseinput):
    """wenn irgendwas (any) in rezept.Gang das beinhaltet was der input war dann gibs raus
   any ----> auch wenn man "des" eingibt zeigt er dessert an weil des dadrin steckt.
   ohne any würde er dann nichts raus geben."""
    gang = courseinput.strip().lower()
    return any(
        rezept.gang.strip().lower() == gang
        for rezept in recipes
    )

######## FILTER ####################################################################################################################################################

def filter_recipe_by_name(repo: JsonRezeptRepository, recipe: str) -> List[model.Rezept]:
    """wollte eigentlich mit "any" arbeiten, aber teiltreffer ("Bro" eingabe zeigt "Brokkoli" an)
    werden auch durch "in" ermöglicht. any macht kein sinn weil gerichte.Name keine Liste
     sondern ein String ist, bei Zutaten machte es Sinn weil Zutaten eine Liste ist.(any = irgendeins aus (der liste)/ in = irgendetwas im (string))
     """
    recipe = recipe.strip().lower()
    return [r for r in repo.all() if recipe in r.name.strip().lower()]

def filter_recipe_by_course(repo: JsonRezeptRepository, courseinput: str) -> List[model.Rezept]:
    """Siehe filter_rezepte_nach_zutaten, selbe sache nur ohne aus einer liste(gerichte)
   eine weitere liste(wie unten die zutatenliste) aufrufen zu müssen."""
    course = courseinput.strip().lower()
    return [r for r in repo.all() if r.gang.strip().lower() == course]

def filter_recipe_by_ingredient(repo: JsonRezeptRepository, ingredientinput: List[str]) -> List[model.Rezept]:
    """ rezept for rezept in storage.Gerichte > geh jedes rezept durch was gespeichert wurde.(s.Gerichte = rezeptsammlung / rezept for rezept = jedes Rezept einzeln durchgehen)
    any(zutat in einzelne_zutat = gibt es die gesuchten Zutaten im Rezept? ///// for einzelne_zutat in rezept.Zutaten) = guck jede Zutat des Rezepts an.
    all(any(bla)for zutat in zutaten) =  sind ALLE gesuchten Zutaten in diesem Rezept?""" 
    zutatenwahl = [z.strip().lower() for z in ingredientinput if z.strip()]
    return [
        rezept
        for rezept in repo.all()
        if all(
            any(zutat in einzelne_zutat.name.strip().lower() for einzelne_zutat in rezept.zutaten)
            for zutat in zutatenwahl
        )
    ]

def dynamic_search_recipes(repo: JsonRezeptRepository, name: str | None = None ,gang:str | None = None ,zutaten: List[str] | None = None) -> List[model.Rezept]:

    recipes = repo.all()                #macht das recipes eine Kopie der Liste aller Rezepte ist , wenn jetzt bei "name" schon Sushibowl als Treffer übernommen wird,
                                        #ist Sushibowl quasi aus der recipes Liste raus und kann bei der "gang" Suche nicht nochmal übernommen werden.

    if name:
        recipes =[recipe for recipe in recipes if name in recipe.name.strip().lower()]
            
    if gang:
        recipes =[recipe for recipe in recipes if gang in recipe.gang.strip().lower()]

    if zutaten:
        recipes =[recipe for recipe in recipes if all(any(zutat in einzelne_zutat.name.strip().lower() for einzelne_zutat in recipe.zutaten)
            for zutat in zutaten)]

    return recipes
                    

######## ÄNDERUNGEN ################################################################################################################################################

    
def create_recipe(
    repo: JsonRezeptRepository,
    recipe_datas: schemas.RecipeCreate,
) -> model.Rezept:
    zutaten = [model.Zutaten(name=z.zutatenname,menge=z.menge,einheit=z.einheit) for z in recipe_datas.zutaten]
    
    new_recipe = model.Rezept(
        name=recipe_datas.name,
        zutaten=zutaten,
        zubereitung=recipe_datas.zubereitung,
        gang=recipe_datas.gang,
        notizen=recipe_datas.notizen
    )

    repo.add(new_recipe)
    repo.save()
    return new_recipe

def delete_recipe(repo: JsonRezeptRepository, recipename : str) -> bool:

    recipe = find_exact_recipe(repo,recipename)

    if recipe is None:
        return False
    
    repo.remove(recipe)
    repo.save()
    return True

def update_recipe(repo: JsonRezeptRepository, update_datas: schemas.UpdateCreate) -> bool:
    recipe_to_update = find_exact_recipe(repo,update_datas.searched_recipe)
    if recipe_to_update is None:
        return  False
    else:
        if update_datas.recipeattribute != "zutaten":
            if not hasattr(recipe_to_update,update_datas.recipeattribute):
                return False
        
            setattr(recipe_to_update,update_datas.recipeattribute,update_datas.change)
            

        if update_datas.recipeattribute == "zutaten" and update_datas.ingredient_attribute and update_datas.searched_ingredient is not None:
            for ingredient in recipe_to_update.zutaten:
                if ingredient.name.lower().strip() == update_datas.searched_ingredient.lower().strip():
                    if not hasattr(ingredient,update_datas.ingredient_attribute):
                        return False
                
                    setattr(ingredient,update_datas.ingredient_attribute,update_datas.change)
                    repo.save()
                    return True
            return False
    
    repo.save()
    return True

