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

    recipes = repo.all()

    for xyz in recipes:
        if xyz.name.lower().strip() == recipename.lower().strip():
            return xyz
        else:
            return None
        
def find_ingredient_in_all_recipes(repo: JsonRezeptRepository, ingredientname: str) -> Optional[model.Zutaten]:
        
        recipes = repo.all()

        for recipe in recipes:
            for zutat in recipe.zutaten:
                if ingredientname.strip().lower() == zutat.name.strip().lower():
                    return zutat
        return None

def find_ingredient_in_one_recipe(repo: JsonRezeptRepository, recipename:str,ingredientname:str) -> Optional[model.Zutaten]:
        
        recipes = repo.all()

        for recipe in recipes:
            if recipename.lower().strip() == recipe.name.strip().lower():
                for zutat in recipe.zutaten:
                    if ingredientname.strip().lower() == zutat.name.lower().strip():
                        return zutat
                return None    
        return None

######## VALIDIERUNG ##############################################################################################################################################
def check_recipename(repo: JsonRezeptRepository,recipename) -> bool:
    if find_exact_recipe(repo,recipename):
        return True
    return False

def check_attribute(repo: JsonRezeptRepository,rezeptname,attributname) -> bool:
    if hasattr(find_exact_recipe(repo,rezeptname),attributname) is not None:
        return True
    return False

def check_ingredient_attribute(repo: JsonRezeptRepository,recipename,ingredientname,attributename) -> bool:
    if hasattr(find_ingredient_in_one_recipe(repo,recipename,ingredientname),attributename) is not None:
        return True
    return False

def check_ingredient_in_recipe(repo: JsonRezeptRepository,recipename,ingredientname) -> bool:
    if find_ingredient_in_one_recipe(repo,recipename,ingredientname)is not None:
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

#all hits service funktion noch auf die anderen layer übertragen und im swagger testen

def all_hits_recipes(repo: JsonRezeptRepository, name: str | None = None , gang:str | None = None , zutaten: List[str] | None=None) -> List[model.Rezept]:

    recipes = repo.all()

    hit_list= []

    for xyz in recipes:
        if name == None:
            continue
        else:
            if name in xyz.name.strip().lower():
                hit_list.append(xyz)

    for xyz in recipes:
        if gang == None:
            continue
        else:
            if gang in xyz.gang.strip().lower()and xyz not in hit_list:
                hit_list.append(xyz)
            

    for xyz in recipes:                                 # für variable in allen rezepten
        if zutaten == None:
            continue
        else:
                for gesuchte_zutat in xyz.zutaten:      # für variable in den zutaten aller rezepte    
                    for aktuelle_zutat in zutaten:      # für variable in den angegebenen zutaten ( da man ja mehrere angeben kann wird hierdurch durch jede eingegebene gesuchte zutat iteriert und einzelne_zutat ist dann jeweils eine zutat der eingegebenen zutatenliste)
                        if aktuelle_zutat in gesuchte_zutat.name.strip().lower() and xyz not in hit_list:  # wenn die aktuelle zutat aus zutaten teiltreffer mit zutatennamen in irgend nem rezept hat
                            hit_list.append(xyz)        #ab inne liste rinne
                        
    
    return hit_list

                    

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

