package main;

import java.nio.file.Files;
import java.nio.file.Path;

import model.Rezept;
import repository.RezeptRepository;


public class Main {
    public static void main(String[] args) throws Exception {
        Path jsonPath = args.length > 0 ? Path.of(args[0]) : Path.of("C:\\Users\\ggord\\OneDrive\\Desktop\\VSC_Projekte\\Data\\RezeptData\\rezepte.json");
        if (!Files.exists(jsonPath)) {
            throw new IllegalStateException(
                    "Rezepte-Datei nicht gefunden: " + jsonPath.toAbsolutePath() +
                            " (uebergib Pfad als erstes Argument oder lege rezepte.json im Projektordner ab)"
            );
        }

        RezeptRepository repository = new RezeptRepository(jsonPath);

        var rezepte = repository.ladeAlle();

        for (Rezept r : rezepte) {
            System.out.println(r.getName());
            r.getZutaten().forEach(z ->
                    System.out.println("  - " + z.getMenge() + " " +
                            z.getEinheit() + " " + z.getName()));
        }
    }
}
