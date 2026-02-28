package main.model;


public class Zutat
{
    String name;
    String menge;
    String einheit;
    
        @Override
    public String toString(){
        return menge + "" + einheit + " " + name;
    }

    public Zutat(String einheit,String menge,String name)
    {
        this.name = name;
        this.menge = menge;
        this.einheit = einheit;
    }
    public void anzeigen()
    {
        System.out.println(menge + " " + einheit + " " + name);
    }
}

