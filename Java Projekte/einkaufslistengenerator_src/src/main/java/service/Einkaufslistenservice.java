package service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import model.Rezept;
import model.RezeptZutat;

public class Einkaufslistenservice{
    //public = öffentlich | Map<String,Double> = Map is wie dict bei python, Datentyp mit Text + Zahl die zusammenhängen ( hier Einheit und menge )
    //zusammenfassen = der Name der Funktion | (List<Rezept> rezepte) = Parameter der Methode , also Platzhhalter für die Rezepte dessen Zutaten zusammengefasst werden sollen.
    public Map<String, Double> zusammenfassen(List<Rezept> rezepte) {
        Map<String, Double> result = new HashMap<>(); // leere Map Datentyp wird erstellt in den dann die passenden Zutaten reingeschrieben werden
        // for r in rezepte for z in r.zutat als Java 
        // für jedes Rezept r in rezepte gib mir die passenden zutaten ( r.getZutaten) aus RezeptZutat
        for (Rezept r : rezepte) {
            for (RezeptZutat z : r.getZutaten()) {
                Double mengeAlsZahl = z.getMengeAlsZahl();
                if (mengeAlsZahl == null) {
                    continue; // z.B. "nach Bedarf" nicht numerisch summierbar
                }
                // klassisches .split().lower() ding aus python nur mit Java
                // übrigens durch getName bedarf es keiner [:-2] Sachen
                // wie bei Python um Zutatnamen richtig zu erfassen.
                String name = z.getName().trim().toLowerCase();
                String unit = z.getEinheit().trim().toLowerCase();
                // Variable Key merged Name und Einheit mit | als Trennzeichen
                String key = name + "|" + unit;
                //result = variable des endprodukts > wird dann unten returned | .put sagt einfach "speichere folgendes noch zur der Variable" ( hier die Menge bzw GetMengeAlsZahl)
                // result.getOrDefault (key, defaultValue) = falls kein getMengeAlsZahl existiert, nimm den Wert 0.0
                result.put(
                    key,
                    result.getOrDefault(key, 0.0) + mengeAlsZahl
                );
            }
        }

        return result;

    }
}
