package main.main;

import main.model.Rezept;
import main.storage.Storage;

public class Main {

    public static void main(String[] args) {
        // generiert aus der theoretischen Klasse ein praktisches Objekt
        // Storage wird hier quasi im aktiven Programm aufrufen initialisiert,
        // also die Daten des Storage werden in das programm geladen. 
        // (Klasse) = Bauplan des Hauses 
        // (Storage storage = new Storage();) = baut das Haus 
        Storage storage = new Storage();  
             
        for (Rezept r : storage.getRezepte()) 
        {
            System.out.println(r.getName());
        }
        
        for (Rezept r : storage.getRezepte()) 
        {
            System.out.println(r);
        }

    }
}
