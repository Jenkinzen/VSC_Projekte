package model;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class RezeptZutat {
    private final String name;
    private final String menge;     // STRING wegen "nach Bedarf"
    private final String einheit;

    @JsonCreator
    public RezeptZutat(
            @JsonProperty("name") String name,
            @JsonProperty("menge") String menge,
            @JsonProperty("einheit") String einheit
    ) {
        this.name = name;
        this.menge = menge;
        this.einheit = einheit;
    }

    public String getName() { return name; }
    public String getMenge() { return menge; }
    public String getEinheit() { return einheit; }

    // optional: versuchen, Zahl zu extrahieren
    public Double getMengeAlsZahl() {
        try {
            return Double.parseDouble(menge);
        } catch (Exception e) {
            return null; // z.B. "nach"
        }
    }
}