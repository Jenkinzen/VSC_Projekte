package main.service;

import java.util.ArrayList;
import java.util.List;
import main.model.Rezept;
import main.storage.Storage;

public class Service 
{
    //wieso private storage?
    private Storage storage = new Storage();

    public List<String> filterNachRezeptName(String suchwort)
    {
        List<String> namen = new ArrayList<>();
        for (Rezept r : storage.getRezepte()) {
            if (r.getName().toLowerCase().contains(suchwort.toLowerCase())){
                namen.add(r.getName());
            }
        }
        return namen;
    }
}
