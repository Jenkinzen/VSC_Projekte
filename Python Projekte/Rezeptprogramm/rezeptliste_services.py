import rezeptliste_model as model
from typing import List, Optional
import rezeptliste_schemas as schemas

#LIST COMP CHEAT SHEET



#result = []                    # wird unten durch [] in der die LC steht ersetzt
#for r in repo.all():           # steht unten einfach hintereinander
#   if r.gang == "Dessert":     # steht unten einfach hintereinander
#       result.append(r.name)   # wird unten durch r.name am Anfang ersetzt

#[WAS for WERT in QUELLE if BEDINGUNG]
#[r.name for r in repo.all() if r.gang == "Dessert"]

######## BASISZUGRIFF - LESEN #################################################################################################################################

 
def find_exact_recipe(repo, recipe_id: int) -> Optional[model.Rezept]:

    recipes = repo.all()

    for recipe in recipes:
        if recipe.rezept_id == recipe_id:
            return recipe
    else:
        return None
        
def find_exact_ingredient(repo,recipe: model.Rezept, zutat_id: int) -> Optional[model.Zutaten]:


    for ingredient in recipe.zutaten:
        if zutat_id == ingredient.zutat_id:
            return ingredient
    else:
        return None

######## FILTER ####################################################################################################################################################

def match_all_search_recipes(repo, name: str | None = None ,gang:str | None = None ,zutaten: List[str] | None = None) -> List[model.Rezept]:

    recipes = repo.all()                #macht das recipes eine Kopie der Liste aller Rezepte ist , wenn jetzt bei "name" schon Sushibowl als Treffer übernommen wird,
                                        #ist Sushibowl quasi aus der recipes Liste raus und kann bei der "gang" Suche nicht nochmal übernommen werden.

    if name:
        recipes =[recipe 
                  for recipe in recipes 
                  if name.strip().lower() in recipe.name.strip().lower()]
            
    if gang:
        recipes =[recipe 
                  for recipe in recipes 
                  if gang.strip().lower() in recipe.gang.strip().lower()]

    if zutaten:
        recipes =[recipe 
                  for recipe in recipes 
                  if all(any(zutat in           # check ob ALLE(all) erfragten Zutaten IRGENDWO(any) in der Zutatenliste des Rezeptes stehen.
                                                # ohne all würde man nicht validieren das ALLE gesuchten Zutaten auch True sind. (sind ALLE true?)
                                                # ohne any würde man nicht checken ob es IRGENDWO in der Liste eine Zutat gibt die True zurück gibt. (ist das irgendwo TRUE?)
                                                # all checkt ob alle any rückgabewerte True sind , wenn ja gibt all auch True zurück und somit wird validiert das alle
                                                # gesuchten Zutaten in diesem Rezept vorhanden sind.

                             einzelne_zutat.name.strip().lower() for einzelne_zutat in recipe.zutaten) 
            for zutat in zutaten)]

    return recipes

def match_any_search_recipes(repo, name: str | None = None , gang:str | None = None , zutaten: List[str] | None=None) -> List[model.Rezept]:

    recipes = repo.all()

    hit_list= []

    for recipe in recipes:
        if name == None:
            continue
        else:
            if name.strip().lower() in recipe.name.strip().lower():
                hit_list.append(recipe)

    for recipe in recipes:
        if gang == None:
            continue
        else:
            if gang.strip().lower() in recipe.gang.strip().lower()and recipe not in hit_list:
                hit_list.append(recipe)
            

    for recipe in recipes:                                 # für variable in allen rezepten
        if zutaten == None:
            continue
        else:
                for gesuchte_zutat in recipe.zutaten:      # für variable in den zutaten aller rezepte    
                    for aktuelle_zutat in zutaten:      # für variable in den angegebenen zutaten ( da man ja mehrere angeben kann wird hierdurch durch jede eingegebene gesuchte zutat iteriert und einzelne_zutat ist dann jeweils eine zutat der eingegebenen zutatenliste)
                        if aktuelle_zutat.strip().lower() in gesuchte_zutat.name.strip().lower() and recipe not in hit_list:  # wenn die aktuelle zutat aus zutaten teiltreffer mit zutatennamen in irgend nem rezept hat
                            hit_list.append(recipe)        #ab inne liste rinne
                        
    
    return hit_list

                    

######## ÄNDERUNGEN ################################################################################################################################################

    
def create_recipe(
    repo,
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

    created_recipe = repo.add(new_recipe)

    if hasattr(repo, "save"):                   #hasattr kann auch methoden prüfen -> prüft ob das repo ne "save" methode hat ( die nur das json repo hat aber nicht das sql repo) damit man die Funktion über beide repos nutzen kann.
        repo.save()

    return created_recipe

def delete_recipe(repo, recipe_id : int) -> bool:

    recipe = find_exact_recipe(repo,recipe_id)

    if recipe is None:
        return False
    
    repo.remove(recipe)
    
    if hasattr(repo, "save"):
        repo.save()

    return True

def update_recipe(repo, update_datas: schemas.RecipeUpdate) -> bool:
    recipe_to_update = find_exact_recipe(repo,update_datas.rezept_id)
    if recipe_to_update  is None:
        return  False

    if update_datas.aenderung is None:
        return False
    
    if update_datas.aenderung.strip().lower() not in  ["rezept","zutat"]:
        return False
    
    
    
    if update_datas.aenderung.lower().strip() == "rezept":
        if any([update_datas.name_neu is not None,update_datas.zubereitung_neu is not None,update_datas.gang_neu is not None,update_datas.notizen_neu is not None]):
            if update_datas.name_neu is not None:
                setattr(recipe_to_update,"name",update_datas.name_neu)
            if update_datas.zubereitung_neu is not None:
                setattr(recipe_to_update,"zubereitung",update_datas.zubereitung_neu)
            if update_datas.gang_neu is not None:
                setattr(recipe_to_update,"gang",update_datas.gang_neu)
            if update_datas.notizen_neu is not None:
                setattr(recipe_to_update,"notizen",update_datas.notizen_neu)
        else:
            return False
    
    elif update_datas.aenderung.lower().strip() == "zutat":
        if update_datas.zutat_id is not None:
            ingredient_to_change = find_exact_ingredient(repo,recipe_to_update,update_datas.zutat_id)
            if ingredient_to_change is not None:
                for ingredientattribute in update_datas.zutaten:        #für das attribut, aus den zutatsattributen, das verändert werden soll
                    if any([ingredientattribute.name_neu is not None,ingredientattribute.menge_neu is not None,ingredientattribute.einheit_neu is not None]): 
                        if ingredientattribute.name_neu is not None:
                            setattr(ingredient_to_change,"name",ingredientattribute.name_neu)
                        if ingredientattribute.menge_neu is not None:
                            setattr(ingredient_to_change,"menge",ingredientattribute.menge_neu)
                        if ingredientattribute.einheit_neu is not None:
                            setattr(ingredient_to_change,"einheit",ingredientattribute.einheit_neu)  
                    else:
                        return False
            else:
                return False
        else:
            return False
    else:
        return False
    
    repo.update(recipe_to_update)        
    return True                
                              



