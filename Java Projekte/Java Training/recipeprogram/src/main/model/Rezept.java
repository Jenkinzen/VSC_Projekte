package main.model;

import java.util.ArrayList;

public class Rezept
    {
        String name;
        ArrayList<Zutat> zutaten;  // so einfach integriert man eine Klasse in eine andere wtf
        String zubereitung;            // ArrayList<Zutat> zutaten > sonst kann man nur einzelne Zutaten speichern, keine Liste.
        String notizen;

        @Override
        public String toString()
        {
            return name + "\n" + zutaten + "\n" + zubereitung + "\n" + notizen;
        }

        public Rezept(String name,String zubereitung,String notizen) //keine Zutaten im Konstruktor
        {                                                            // die werden ja manuell durch addZutat erzeugt.                             
        this.name = name;
        this.zutaten = new ArrayList<>();           // beim aufrufen des Rezeptes wird die Liste der zugehörigen
        this.zubereitung = zubereitung;             // Zutaten in eine neue ArrayList gepackt.
        this.notizen = notizen;
        }

        public void addZutat (Zutat z)
        {
            zutaten.add(z);
        }

        public void anzeigen()                      // wird in der funktion von Zutaten aufgerufen um dort Zutaten anzuzeigen
        {
            System.out.println("Rezept"+ name);

            for (Zutat z : zutaten) 
                {
                    z.anzeigen();
                }
        }
    }
