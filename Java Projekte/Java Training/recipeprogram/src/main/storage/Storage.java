package main.storage;

import java.util.ArrayList;
import main.model.Rezept;
import main.model.Zutat;

public class Storage     // Klassenrumpf = Nur das Grundkonzept, das Gerüst oder die Blaupause einer Klasse,
{                       // beschreibt wie Objekte aussehen, aber kann selbst nichts.


    // früher wär es ArrayList<Rezept> rezepte = new ArrayList<Rezept>(); gewesen,
    // mittlerweile übernimmt Java den Elementtyp links (also <Rezept>) automatisch für rechts weshalb man nur <> brauch
    // deklariert das in die ArrayList nur Objekte vom Typ Rezept und dessen Unterklassen(wie Zutat) rein darf.
    private final ArrayList<Rezept> rezepte = new ArrayList<>(); 

    public Storage()
    {
        Rezept sushibowl = new Rezept(

            "Sushibowl",
            "irgendwas",
            "irgendwas");

        sushibowl.addZutat(new Zutat("Reis","150","g"));

        rezepte.add(sushibowl);

        Rezept salat = new Rezept(

        "Salat",
        "Schnibbeln",
        "bla");

        salat.addZutat(new Zutat("1","Kopf","Salat"));
        rezepte.add(salat);


        Rezept kokoscurrypfanne = new Rezept(

        "Kokos-Curry-Pfanne",
        "Alles kleinschnibbeln-Zwiebeln glasig anschwitzen-Rest anbraten-Soße anrühren und abschmecken-essen",
        "Kräutersaitlinge,Rosensaitlinge,Enokis oder Austernpilze eignen sich hervorragend für dieses Gericht");

        kokoscurrypfanne.addZutat(new Zutat("500","ml","Kokosmilch"));
        kokoscurrypfanne.addZutat(new Zutat("150","ml","Currypaste"));
        kokoscurrypfanne.addZutat(new Zutat("250","g","Pilze"));

        rezepte.add(kokoscurrypfanne);
    }

    

    public ArrayList<Rezept> getRezepte()
    {
        return rezepte;
    }
}

