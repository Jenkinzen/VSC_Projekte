from dataclasses import dataclass
from typing import List, Optional
import textwrap


@dataclass
class Zutaten:
    name: str
    menge: Optional[str] = None
    einheit: Optional[str] = None
    zutat_id: int | None = None
    rezept_id: int | None = None



@dataclass
class Rezept:
    name: str
    zutaten: List[Zutaten]
    zubereitung: str
    gang: str
    notizen: str = ""
    rezept_id: int | None = None
    

