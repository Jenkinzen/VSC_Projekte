package model;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Rezept {
    private final String name;
    private final String gang;
    private final String zubereitung;
    private final String notizen;
    private final List<RezeptZutat> zutaten;

    @JsonCreator
    public Rezept(
            @JsonProperty("name") String name,
            @JsonProperty("gang") String gang,
            @JsonProperty("zubereitung") String zubereitung,
            @JsonProperty("notizen") String notizen,
            @JsonProperty("zutaten") List<RezeptZutat> zutaten
    ) {
        this.name = name;
        this.gang = gang;
        this.zubereitung = zubereitung;
        this.notizen = notizen;
        this.zutaten = zutaten == null ? List.of() : List.copyOf(zutaten);
    }

    public String getName() { return name; }
    public String getGang() { return gang; }
    public String getZubereitung() { return zubereitung; }
    public String getNotizen() { return notizen; }
    public List<RezeptZutat> getZutaten() { return zutaten; }

    @Override
    public String toString() {
        return "Rezept{" +
                "name='" + name + '\'' +
                ", gang='" + gang + '\'' +
                ", zubereitung='" + zubereitung + '\'' +
                ", notizen='" + notizen + '\'' +
                ", zutaten=" + zutaten +
                '}';
    }
}
