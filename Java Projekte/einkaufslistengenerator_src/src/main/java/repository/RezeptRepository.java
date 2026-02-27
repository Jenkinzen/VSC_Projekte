package repository;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import model.Rezept;

public class RezeptRepository {

    private final Path jsonPath;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public RezeptRepository(Path jsonPath) {
        this.jsonPath = jsonPath;
    }

    public List<Rezept> ladeAlle() {
        try {
            JsonNode root = objectMapper.readTree(jsonPath.toFile());

            if (root.isArray()) {
                return objectMapper.convertValue(root, new TypeReference<List<Rezept>>() {});
            }
            if (root.isObject() && root.has("rezepte")) {
                return objectMapper.convertValue(root.get("rezepte"), new TypeReference<List<Rezept>>() {});
            }

            throw new IllegalStateException("Ungueltiges JSON-Format. Erwartet: Array oder Objekt mit Feld 'rezepte'.");
        } catch (IOException e) {
            throw new IllegalStateException("Konnte Rezepte nicht laden: " + jsonPath.toAbsolutePath(), e);
        }
    }
}
