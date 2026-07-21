from __future__ import annotations

import json
import sqlite3 as sql
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

    def all(self) -> List[model.Rezept]:                       # def alle(self) -> List[model.Rezept]: ist quasi DATENTYP OUTPUT: ArrayList<Model.Rezept> METHODENNAME: alle INPUTPARAMETER(self)[self im bezug auf die repository class, also Repository Objekt].
        # Optional: return list(self._gerichte) um Kopie zu geben
        return self._gerichte

    def add(self, recipe: model.Rezept) -> model.Rezept:

        highest_rezept_id = 0

        for gericht in self._gerichte:
            
            if gericht.rezept_id is not None:
                if gericht.rezept_id > highest_rezept_id:
                    highest_rezept_id = gericht.rezept_id
                                
        recipe.rezept_id = highest_rezept_id + 1


        for zutat in recipe.zutaten:
                if zutat.rezept_id is None:
                    zutat.rezept_id = recipe.rezept_id
                    
        highest_ingredient_id = 0

        for zutat in recipe.zutaten:
            if zutat.zutat_id is None:
                zutat.zutat_id = 1
                highest_ingredient_id = 1
            else:
                if zutat.zutat_id < highest_ingredient_id: 
                    zutat.zutat_id = highest_ingredient_id + 1
                
        self._gerichte.append(recipe)
        return recipe

    def remove(self, recipe: model.Rezept) -> None:
        self._gerichte.remove(recipe)

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

    def update(self,rezept: model.Rezept) -> None:
        self.save()

    def __getitem__(self, index: int) -> model.Rezept:
        return self._gerichte[index]

    def __len__(self) -> int:
        return len(self._gerichte)










class SqlRezeptRepository:
    def __init__(self,db_datei: Path):
        self._db_datei = db_datei
        self._connection = sql.connect(self._db_datei,check_same_thread=False)     #hier kommt kein DB pfad in die klammer, der wird in rezeptliste_api definiert (SoC + universales repo für verschiedene DB's)
        self._connection.row_factory = sql.Row                                     # dafür damit man später spalten als name lesen kann
        self._connection.execute("PRAGMA foreign_keys = ON")                       # check_same_thread=False ist dafür das mehrere Programmprozesse gleichzeitig mit sql connecten können ohne das sql stresst ( quasi TCP aber bezogen auf Programmprozesse und nicht Serververbindungen)
        self.create_tables() 

    def create_tables(self):
        self._connection.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,          
                                 name TEXT NOT NULL UNIQUE,
                                 zubereitung TEXT NOT NULL,
                                 gang TEXT NOT NULL,
                                 notizen TEXT)
                                 """)
                                                                    # INTEGER PRIMARY KEY AUTOINCREMENT -> jedes Gericht bekommt automatisch eine eigene ID zugewiesen, jede Zeile kriegt
                                                                    # eine eigene Zahl zugewiesen / UNIQUE -> darf nur 1 mal so vorkommen ( damit man nicht mehrere gleiche Rezeptnamen in die SQL packen kann)
        self._connection.execute("""
                                 CREATE TABLE IF NOT EXISTS recipe_ingredients(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 recipe_id INTEGER NOT NULL,
                                 zutatenname TEXT NOT NULL,
                                 menge TEXT,
                                 einheit TEXT,
                                 FOREIGN KEY (recipe_id) REFERENCES recipes(id))
                                 """)
        
        self._connection.commit()

    def all(self) -> list[model.Rezept]:
        recipe_rows = self._connection.execute(
            """SELECT id AS recipe_id, name, zubereitung, gang, notizen
            FROM recipes
            """
        ).fetchall() # hol mir die oben SELECTeten Daten alle ( gibt auch fetchone (erste Datei[mit Datei ist eine Zeile gemeint also ein Rezept mit allen attributen]))

        rezepte = []

        for recipe_row in recipe_rows:
            ingredient_rows = self._connection.execute(
                """
                SELECT id AS ingredient_id,zutatenname, menge, einheit
                FROM recipe_ingredients
                WHERE recipe_id = ?
                """,(recipe_row["recipe_id"],)
            ).fetchall()

            zutaten = []

            for row in ingredient_rows:
                zutat = model.Zutaten(
                    zutat_id=row["ingredient_id"],
                    rezept_id=recipe_row["recipe_id"],
                    name=row["zutatenname"],
                    menge= row["menge"],
                    einheit=row["einheit"]
                    )
                zutaten.append(zutat)


            

            rezept = model.Rezept(
                rezept_id=recipe_row["recipe_id"],
                name=recipe_row["name"],
                zutaten=zutaten,
                zubereitung=recipe_row["zubereitung"],
                gang=recipe_row["gang"],
                notizen=recipe_row["notizen"]
            )

            rezepte.append(rezept)

        return rezepte

    def add(self,rezept: model.Rezept):
        cursor = self._connection.execute("""
                                            INSERT INTO recipes (name,zubereitung,gang,notizen)
                                            VALUES(?,?,?,?)""",(
                                            rezept.name,
                                            rezept.zubereitung,
                                            rezept.gang,
                                            rezept.notizen))
        
        recipe_id = cursor.lastrowid        # also lastrowid = die automatisch durch sql zugeteilte id des eben erstellten rezeptes

        for zutat in rezept.zutaten:
            self._connection.execute("""
                                     INSERT INTO  recipe_ingredients (recipe_id, zutatenname, menge, einheit)
                VALUES (?,?,?,?)
                """,
                (
                    recipe_id,
                    zutat.name,
                    zutat.menge,
                    zutat.einheit
                )
            )
            
        self._connection.commit()
        return rezept

    def update(self,rezept: model.Rezept):
        self._connection.execute("""
            UPDATE recipes SET name = ?,zubereitung = ?,gang = ?,notizen = ? WHERE id = ?""",
            (rezept.name,rezept.zubereitung,rezept.gang,rezept.notizen,rezept.rezept_id,))
        
        for zutat in rezept.zutaten:
            self._connection.execute("""
                UPDATE recipe_ingredients SET zutatenname = ?,menge = ?, einheit = ? WHERE recipe_id = ?""",
                (zutat.name,zutat.menge,zutat.einheit,zutat.rezept_id))
            
        self._connection.commit()

    def remove(self,rezept: model.Rezept) -> None:
        recipe_row = self._connection.execute("""
                                    SELECT id
                                 FROM recipes
                                 WHERE name = ?
                                    """,                    # erst in """ das sql Statement mit ? als variablenplatzhalter und danach "," und dann in klammern die variable, bei mehreren ? chronologisch in klammern (variable1,variable2,etc..) 
                                    (rezept.name,)          # auch bei 1 variable ein "," danach einfach klammer zu machen weil in der klammer immer ein Tupel stehen muss. 
                                    ).fetchone()
        if recipe_row is None:
            return
        
        recipe_id = recipe_row["id"]

        self._connection.execute(
            """DELETE FROM recipe_ingredients
            WHERE recipe_id = ?
            """,
            (recipe_id,)
        )

        self._connection.execute(
            """DELETE FROM recipes
            WHERE id = ?
            """,
            (recipe_id,)
        )

        self._connection.commit()

 
