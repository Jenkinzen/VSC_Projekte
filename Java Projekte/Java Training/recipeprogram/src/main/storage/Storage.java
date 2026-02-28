package main.storage;

import java.util.ArrayList;
import main.model.Rezept;
import main.model.Zutat;

public class Storage     // Klassenrumpf = Nur das Grundkonzept, das Gerüst oder die Blaupause einer Klasse,
{                       // beschreibt wie Objekte aussehen, aber kann selbst

    private final ArrayList<Rezept> rezepte = new ArrayList<>();

    public Storage()
    {
        Rezept r = new Rezept(

            "Sushibowl",
            "irgendwas",
            "irgendwas");

        r.addZutat(new Zutat("Reis","150","g"));

        rezepte.add(r);

        Rezept s = new Rezept(

        "Salat",
        "Schnibbeln",
        "bla");

        s.addZutat(new Zutat("Salat","1","Kopf"));
        rezepte.add(s);

        Rezept g = new Rezept(

        "Kokos-Curry-Pfanne",
        "-Alles kleinschnibbeln-Zwiebeln glasig anschwitzen-Rest anbraten-Soße anrühren und abschmecken-essen",
        "Kräutersaitlinge,Rosensaitlinge,Enokis oder Austernpilze eignen sich hervorragend für dieses Gericht");

        g.addZutat(new Zutat("500","ml","Kokosmilch"));
        g.addZutat(new Zutat("150","ml","Currypaste"));
        g.addZutat(new Zutat("250","g","Pilze"));
    }


    public ArrayList<Rezept> getRezepte()
    {
        return rezepte;
    }
}

