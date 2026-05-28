import rezeptliste_model as model
import rezeptliste_storage as storage
from typing import List, Optional
from rezeptliste_repository import JsonRezeptRepository




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

def find_recipe(repo: JsonRezeptRepository, recipename: str) -> Optional[model.Rezept]:

    return repo.find_recipe_by_input(recipename)


######## VALIDIERUNG ##############################################################################################################################################
def check_recipename(repo: JsonRezeptRepository,recipename) -> bool:
    if repo.find_recipe_by_input(recipename):
        return True
    return False

def check_attribute(repo: JsonRezeptRepository,rezeptname,attributname) -> bool:
    if hasattr(find_recipe(repo,rezeptname),attributname) is not None:
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

######## ÄNDERUNGEN ################################################################################################################################################


    """In die Leere Zutatenliste kommen nachher die Objekte aus der Funktion.
        zs variable für Zutat als Text ( wie das 1. x in x for x in Gerichte )
        teile = zs.split() -> die Sachen werden durch leerzeichen gesplittet(also Name,menge,einheit)
        if not teile -> überspringen von allem was sonst zum error führen würde, bzw durch so einen Input
        wird man per continue dann wieder an den Schleifenanfang gebracht für erneuten input.

        zutatenname Zeile -> teile (also die Teile der Zutat: Name, menge, einheit)
          [:-2] heißt NICHT geteilt durch -2 sondern : sagt alles und -2 bis auf die letzten beiden! 
          damit wird jeder Input bis auf die letzten beiden zum "teil" Name hinzugefügt.
          wenns bspw [:-1] wär dann würde die Menge noch mit beim Namen stehen.
          und durch .join davor wird die liste von wörtern zu einem String mit Leerzeichen.
        if len(teile) > 2 -> also mach .join(teile[:-2]) insofern mehr als 2 wörter eingegeben werde.
        else teile[0] -> wenn weniger als 2 wörter eingegeben werden, nimm halt das 1 Wort oder die Leerstelle.
        
        menge -> teile[-2] if len(teile) > 1  --> also vorletztes Teil
            wenn es mehr als 1 teil gibt
            else None -> sonst gibts halt keine Menge. 
            (Unfassbar smart, weil es "Salz , Prise" gibt also angaben ohne Menge,
            aber es gibt keine Angaben ohne Einheit aber mit Menge, weil was will jemand mit
            der aussage " du brauchst 150 Salz")
            
        einheit -> teile[-1] also ist das letzte teil
                if len(teile) >= 2 -> insofern es genau oder mehr als 2 teile gibt.
    """
    
def create_recipe(
    repo: JsonRezeptRepository,
    recipe_datas: dict,
) -> model.Rezept:
    zutaten = [model.Zutaten(z["name"],z.get("menge"),z.get("einheit")) for z in recipe_datas.get("zutaten",[])]
    
    new_recipe = model.Rezept(
        name=recipe_datas["name"],
        zutaten=zutaten,
        zubereitung=recipe_datas["zubereitung"],
        notizen=recipe_datas["notizen"],
        gang=recipe_datas["gang"],
    )

    repo.add(new_recipe)
    repo.save()
    return new_recipe

def delete_recipe(repo: JsonRezeptRepository, recipename : str) -> None:

    recipe = find_recipe(repo,recipename)

    if recipe is None:
        return None
    
    repo.remove(recipe)
    repo.save()

def update_recipe(repo: JsonRezeptRepository, searched_recipe: str,change:str,recipeattribute:str,searched_ingredient:str|None = None,ingredient_attribute:str| None = None ) -> bool:
    updaterezept = find_recipe(repo,searched_recipe)
    if updaterezept is None or recipeattribute is None:
        return  False
    else:
        if recipeattribute != "zutaten":
            if not hasattr(updaterezept,recipeattribute):
                return False
            setattr(updaterezept,recipeattribute,change)
            

        if recipeattribute == "zutaten" and ingredient_attribute and searched_ingredient is not None:
            for xyz in updaterezept.zutaten:
                if not hasattr(xyz,ingredient_attribute):
                    return False
                if xyz.name.lower().strip() == searched_ingredient.lower().strip():
                    setattr(xyz,ingredient_attribute,change)
                    repo.save()
                    return True
            return False
    
    repo.save()
    return True

