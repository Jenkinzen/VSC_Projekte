from pydantic import BaseModel
from typing import Optional


class IngredientCreate(BaseModel):      #Datenstruktur um Zutat zu erstellen
    zutatenname: str
    menge: str | None = None
    einheit: str | None = None
    
class RecipeCreate(BaseModel):          #Datenstruktur um Rezept zu erstellen
    name: str
    zutaten: list[IngredientCreate]
    zubereitung: str
    gang: str
    notizen: str 

class UpdateCreate(BaseModel):          #Datenstruktur um Rezept- bzw Zutatsattribut zu ändern 
    searched_recipe: str
    change:str
    recipeattribute:str
    searched_ingredient:str|None = None
    ingredient_attribute:str| None = None 

class RecipeResponse(BaseModel):        #Datenstruktur um Rezept an den Nutzer auszugeben (bisher gleich wie RecipeCreate aber wird sich noch ändern)
    name: str                           #bspw wenn automatisch vom Server die Zeit erfasst wird wann das rezept erstellt wurde, bei Erstellung macht das der Server selbst
    zutaten: list[IngredientCreate]     # deshalb würde das nicht in der Datenstruktur von "RecipeCreate" auftauchen aber hier weil es ja dem User angezeigt werden soll
    zubereitung: str
    gang: str
    notizen: str 

class MessageResponse(BaseModel):
    info:str