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
    
class MultiUpdateCreateIngredients(BaseModel):
        
        name_neu: str | None = None
        menge_neu: str | None = None  
        einheit_neu: str | None = None

class MultiUpdateCreate(BaseModel):
     aenderung: str
     rezept_id: int 
     zutat_id: int | None = None
     name_neu: str | None = None
     zutaten: list[MultiUpdateCreateIngredients] = []
     zubereitung_neu: str | None = None
     gang_neu: str | None = None
     notizen_neu: str | None = None 

class IngredientResponse(BaseModel):
    zutat_id: int 
    rezept_id: int 
    name: str 
    menge: str | None = None
    einheit: str | None = None

class RecipeResponse(BaseModel):        #Datenstruktur um Rezept an den Nutzer auszugeben
    name: str                           #bspw wenn automatisch vom Server die Zeit erfasst wird wann das rezept erstellt wurde, bei Erstellung macht das der Server selbst
    zutaten: list[IngredientResponse]     # deshalb würde das nicht in der Datenstruktur von "RecipeCreate" auftauchen aber hier weil es ja dem User angezeigt werden soll
    zubereitung: str
    gang: str
    notizen: str 
    rezept_id: int 

class MessageResponse(BaseModel):
    info:str

