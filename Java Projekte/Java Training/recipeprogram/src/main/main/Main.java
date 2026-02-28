package main.main;

import java.util.List;
import main.model.Rezept;
import main.service.Service;
import main.storage.Storage;
public class Main {

    public static void main(String[] args) {
        // generiert aus der theoretischen Klasse ein praktisches Objekt
        // Storage wird hier quasi im aktiven Programm aufrufen initialisiert,
        // also die Daten des Storage werden in das programm geladen. 
        // (Klasse) = Bauplan des Hauses 
        // (Storage storage = new Storage();) = baut das Haus 
        Storage storage = new Storage();  
        Service service = new Service();

        List<String> ergebnis = service.filterNachRezeptName("curry");

        for (String name : ergebnis) {
            System.out.println(name);
        }
        
        for (Rezept r : storage.getRezepte()) 
        {
            System.out.println(r);
        }

    }
}
