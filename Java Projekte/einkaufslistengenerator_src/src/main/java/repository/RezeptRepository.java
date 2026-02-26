package repository;
import java.nio.file.Path;
import java.util.List;

import model.Rezept;

public class RezeptRepository {

    private final Path jsonPath;

    public RezeptRepository(Path jsonPath) {
        this.jsonPath = jsonPath;
    }

    public List<Rezept> ladeAlle() {
        // Hier später JSON laden
        throw new UnsupportedOperationException("JSON-Laden noch nicht implementiert");
    }
}