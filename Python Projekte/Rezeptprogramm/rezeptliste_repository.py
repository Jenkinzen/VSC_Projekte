from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import rezeptliste_model as model

#also... das Repo ist NICHT der Speicher der dictionaries etc. 
#Das Repo ist der aktive Objektspeicher während der Programmausführung, also hat z.b. json dictionary und die umwandlung dessen Inhalt mit Objekten noch nichts
#mit dem Repo zu tun sondern nur mit der json Datei und Python, erst wenn Python das dict in Objekte umwandelt und DANN im Repo speichert 
# JSON DICT = (der passive Langzeitspeicher auf der Festplatte wo die Infos liegen)
# PYTHON -> wandelt Infos aus dem JSON Dict in Objekte um und steckt sie ins Repo.
# REPOSITORY = (der aktive RAM-Memory Speicher während Ausführung)

class JsonRezeptRepository:
    def __init__(self, datei: Path):            # datei: Path  -> ich erwarte ein "Path" Objekt, also den Pfad zur Datei ( hier der Pfad zur rezepte.json)
        self._datei = datei                     # referenz auf den Pfad wo gespeichert wird ( ohne das hier wüssten die methoden save und load nicht WO gesafet und geloaded wird
                                                # [ein wirklicher Pfad zu einem Speicherplatz auf der Festplatte, ist so anders für mich weils vorher ja nur referenzen auf andere Layer waren ])
        self._gerichte: List[model.Rezept] = []         # quasi List<model.Rezept> = new Arraylist<>() in python version | Neue leere Liste wird erstellt in die dann die Rezepte aus dem repo rein geladen werden.

    # ---- Zugriff ----
    def alle(self) -> List[model.Rezept]:                       # def alle(self) -> List[model.Rezept]: ist quasi DATENTYP OUTPUT: ArrayList<Model.Rezept> METHODENNAME: alle INPUTPARAMETER(self)[self im bezug auf die repository class, also Repository Objekt].
        # Optional: return list(self._gerichte) um Kopie zu geben
        return self._gerichte

    def add(self, rezept: model.Rezept) -> model.Rezept:
        self._gerichte.append(rezept)
        return rezept

    def remove(self, rezept: model.Rezept) -> None:
        self._gerichte.remove(rezept)

    def find_by_name(self, rezeptname: str) -> Optional[model.Rezept]:
        needle = rezeptname.strip().lower()                             #eingegebener Rezeptname der gesucht wird.
        for rezept in self._gerichte:                                   # rezept als schleifenvariable
            if rezept.name.strip().lower() == needle:                   # wenn rezeptname in der Liste == gesuchter Begriff , 
                return rezept                                           # return rezept.
        return None

    # ---- Persistenz ----
    def load(self) -> None:
        if not self._datei.exists():
            self._gerichte = []
            return

        with open(self._datei, "r", encoding="utf-8") as f:
            daten = json.load(f)

        gerichte: List[model.Rezept] = []
        for r in daten:
            zutaten = [
                model.Zutaten(
                    z["name"],
                    z.get("menge"),
                    z.get("einheit"),
                )
                for z in r.get("zutaten", [])
            ]

            gerichte.append(
                model.Rezept(
                    name=r["name"],
                    zutaten=zutaten,
                    zubereitung=r["zubereitung"],
                    gang=r["gang"],
                    notizen=r.get("notizen", ""),
                )
            )

        self._gerichte = gerichte

    def save(self) -> None:
        daten = []
        for r in self._gerichte:
            daten.append(
                {
                    "name": r.name,
                    "gang": r.gang,
                    "zubereitung": r.zubereitung,
                    "notizen": r.notizen,
                    "zutaten": [
                        {"name": z.name, "menge": z.menge, "einheit": z.einheit}
                        for z in r.zutaten
                    ],
                }
            )

        with open(self._datei, "w", encoding="utf-8") as f:
            json.dump(daten, f, indent=2, ensure_ascii=False)

    # ---- Komfortzugriff ----
    def __getitem__(self, index: int) -> model.Rezept:
        return self._gerichte[index]

    def __len__(self) -> int:
        return len(self._gerichte)
