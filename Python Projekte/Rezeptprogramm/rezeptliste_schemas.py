from pydantic import BaseModel
from typing import Optional


class IngredientCreate(BaseModel):
    zutatenname: str
    menge: str | None = None
    einheit: str | None = None
    

class RecipeCreate(BaseModel):
    name: str
    zutaten: list[IngredientCreate]
    zubereitung: str
    gang: str
    notizen: str 

class UpdateCreate(BaseModel):
    searched_recipe: str
    change:str
    recipeattribute:str
    searched_ingredient:str|None = None
    ingredient_attribute:str| None = None 


