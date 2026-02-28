package main.model;

import java.util.ArrayList;

public class Rezept
    {
        String rezeptname;
        ArrayList<Zutat> zutaten;  // so einfach integriert man eine Klasse in eine andere wtf
        String zubereitung;            // ArrayList<Zutat> zutaten > sonst kann man nur einzelne Zutaten speichern, keine Liste.
        String notizen;

        public String[] zubereitungsschritteformatieren (String zubereitung)
        {       
        //return String[] teile = zubereitung.split("-"); Da String[] schon oben deklariert werden brauch man das hier nicht
        //"Ofen vorwärmen-Pizzateig ausrollen-belegen[...]" wird hier zu ["Ofen vorwärmen","Pizzateig ausrollen","belegen"]
        return zubereitung.split("-");
        }

        @Override
        public String toString()
        {   // hierdurch werden die einzelnen schritte in ein Array gepackt (Liste von Sätzen)
            String schritte[] = zubereitungsschritteformatieren (zubereitung); 

            // Sammelbehälter für alle Zeilen die entstehen, brauch man da toString nur einen String haben darf,
            // da aber unsere formatierte schritteliste grade in einem Array ist in der jeder Schritt ein eigener String
            // ist, kann so toString nicht damit arbeiten >> also text als leeren Ablageplatz in den wir dann die Schritte
            // formatiert und untereinander aber trotzdem als EINEN String nacheinander rein speichern.
            String text = "";   

            //for-Schleife die jeden Schritt im Array einzeln durch diese Funktion ballert.
            // int i = 0 --> beginne bei index 0 (also dem ersten Element[pcs rechnen ja 0,1,2,3])
            // i < schritte.length ---> lass diese schleife so oft wiederholen wie es einzelne Strings in "schritte" gibt
            // (schritte.length ist das equivalent zu len(schritte) bei python, zählt die teile in einem Array)
            // hier wird schritte.length verwendet, da ein Array eine feste größe hat und somit .length nach erstellen
            // des Arrays ein fester Wert bzw eine Eigenschaft ist (12 Schritte > ins schritte[]array > feste größe: 12)
            // i++ --> bei jeder wiederholung wird der index + 1 gemacht damit jeweils der 1,2,3,4 schritt in der Liste
            // genommen wird.
            for(int i = 0; i < schritte.length; i++)  // i ist übrigens nur eine gängige variable für index, könnte man auch Herbert oder Klabusterbeerenbernd nennen.
                {
                    //text auch nochmal nach dem = weil sonst schritte[1] schritte [0] überschreiben würde und man am Ende nur
                    //den letzten Schritt speichern würde anstatt alle. (.trim() wie .strip() in python)
                    // (i+1) > zum nummerieren damit indexplatz 0 > nummerierungszahl 0+1 = 1 ist.
                    text = text + (i+1) + ". " + schritte[i].trim() + "\n";
                }
            
            String zutatentext = "";

            // hier wird zutaten.size() genutzt, da zutaten eine ArrayList ist 
            // (Dynamische Liste in die geaddet und aus der removed werden kann)
            for(int i = 0; i<zutaten.size();i++)
                {
                    zutatentext = zutatentext + zutaten.get(i) ; //zutatentext + zutaten.get(i) damit die alte zutat nicht überschrieben wird.
                }
            
            return rezeptname + "\n" + zutatentext + "\n" + text + notizen + "\n" ;
        }

        public Rezept(String rezeptname,String zubereitung,String notizen) //keine Zutaten im Konstruktor
        {                                                            // die werden ja manuell durch addZutat erzeugt.                             
        this.rezeptname = rezeptname;
        this.zutaten = new ArrayList<>();           // beim aufrufen des Rezeptes wird die Liste der zugehörigen
        this.zubereitung = zubereitung;             // Zutaten in eine neue ArrayList gepackt.
        this.notizen = notizen;
        }

        public void addZutat (Zutat z)
        {
            zutaten.add(z);
        }

        public void anzeigen()                      
        {
            System.out.println("Rezept"+ rezeptname);

            for (Zutat z : zutaten) 
                {
                    z.anzeigen();
                }
        }

        public String getName()
        {
        return rezeptname;
        }

        public String getZubereitung()
        {
            return zubereitung;
        }

        public String getNotizen()
        {
            return notizen;
        }
    }
