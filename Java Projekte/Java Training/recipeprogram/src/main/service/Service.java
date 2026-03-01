package main.service;

import java.util.ArrayList;
import java.util.List;
import main.model.Rezept;
import main.model.Zutat;
import main.storage.Storage;

public class Service 
{
    //Storage wird generiert damit der Service bspw. getRezepte und generell auf den Storage zugreifen kann
    final Storage storage = new Storage();
    
    // Rückgabetyp der Funktion eine List(e) die Strings speichert
    // (diese Liste existiert noch nicht, es wird nur gesagt das hier ein raus kommt)
    // suchwort > parametervariable
    public List<String> filterNachRezeptName(String suchwort)
    {
        // hier wird die wahre Liste erstellt und kriegt "namen" als Variable
        // ArrayList -> flexible Liste wo geadded und removed werden kann( und geändert ).
        List<String> namen = new ArrayList<>();
        //Rezept = Element der Liste|r = variable
        //storage.getRezepte() = Methode die alle Rezepte liefert
        //für jedes Rezept r aus der Liste storage.getRezepte 
        // Rezept gibt hier das Objekt an was gesucht wird , 
        // es könnten durch storage.getRezepte ja theoretisch 
        // auch andere Objekte gegettet werden  
        for (Rezept r : storage.getRezepte()) {
        //gibste mir dat Rezept wo in dem Namen das steht was ich als 
        //suchwort eingegeben hab
            if (r.getName().toLowerCase().contains(suchwort.toLowerCase())){
                // und addest das in meine Liste "namen"
                namen.add(r.getName());
            }
        }
        // und dann gibste mir den Zettel mit der Liste
        return namen;
    }
    public List<String> filterNachRezeptZutat(String suchwort)
    {
        List<String> namen = new ArrayList<>();
        for (Rezept r : storage.getRezepte()){
                for (Zutat z : r.getZutaten()){
                    if(z.getZutatName().toLowerCase().contains(suchwort.toLowerCase())){
                        namen.add(r.getName());
                    }
                }
            }
        return namen;
    }
}
