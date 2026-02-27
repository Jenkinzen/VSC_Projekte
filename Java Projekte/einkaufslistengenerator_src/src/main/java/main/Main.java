package main;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import repository.RezeptRepository;
import service.Einkaufslistenservice;


public class Main {
    //////////////////////////////////////////////////////////////////MAIN////////////////////////////////////////////////////////////////////////////////////
    public static void main(String[] args) throws Exception {
        Path jsonPath = args.length > 0 ? Path.of(args[0]) : Path.of("C:\\Users\\ggord\\OneDrive\\Desktop\\VSC_Projekte\\Data\\RezeptData\\rezepte.json");
        if (!Files.exists(jsonPath)) {
            throw new IllegalStateException(
                    "Rezepte-Datei nicht gefunden: " + jsonPath.toAbsolutePath() +
                            " (uebergib Pfad als erstes Argument oder lege rezepte.json im Projektordner ab)"
            );
        }
    /////////////////////////////////////////////////////////////////OBJEKT-INSTANZ/////////////////////////////////////////////////////////////////////////
        RezeptRepository repository = new RezeptRepository(jsonPath);
        var rezepte = repository.ladeAlle();

        // Java = alles eine Klasse = Funktionen auch eine Klasse
        // deshalb muss man Funktionsklassen als Objekt erstellen
        // um ihre Funktionen zu nutzen , deshalb Einkaufslistenservice Objekt 
        // erstellen. Wird hier der Aufrufvariable ekservice zugeteilt
        Einkaufslistenservice ekservice = new Einkaufslistenservice();

        // hier wird das oben erstellte Funktionsobjekt genutzt um die 
        // Funktion "zusammenfassen" innerhalb der Einkaufslistenservice Klasse aufzurufen
        Map<String,Double> result = ekservice.zusammenfassen(rezepte);

        // Map.Entry = ein einzelnes Schlüsselwertpaar, also in einer Liste
        // von Zutaten mit Key(Name,Einheit) + Value (Menge) EINE Instanz
        // bspw. Mehl|g, 250.0 | <String,Double> weil es die beiden Datentypen sind.
        // entry = Variablenname,könnte auch "item" o.ä. sein.
        // : < bedeutet "in" , hier "aus dieser Sammlung"
        // result (das was bei ekservice.zusammenfassen raus kommt)
        // .entrySet (ist ne Methode)= gibt alle Einträge als Paare zurück
        // Zusammengefasst: 
        // "FÜR JEDEN EINTRAG(KEY+VALUE) IN DER MAP "result" ,SPEICHERE DEN
        // EINTRAG IN DER VARIABLE "entry" UND FÜHR DEN CODEBLOCK WEITER AUS.
        for (Map.Entry<String, Double> entry : result.entrySet()) {

        // String[] = String Array | parts = Variable 
        // entry.getKey() = nimm dir die Keys (wörter der Map)
        // regex:"\\|" = und teile sie mit dem zeichen | 
        // die \\ werden benötigt da | die Syntax für "oder" ist
        // und \\ signalisiert das das folgende symbol nicht die 
        // funktion meint sondern einfach das symbol |
        String[] parts = entry.getKey().split("\\|"); 

        // hol name, unit , menge raus und speichere sie als einzelvariablen
        String name = parts[0];
        String unit = parts[1];
        double menge = entry.getValue();

        // setz die o.g. einzelvariablen so in einen output
        System.out.println(name + " " + menge + " " + unit);
        }

        

    }
    
}
