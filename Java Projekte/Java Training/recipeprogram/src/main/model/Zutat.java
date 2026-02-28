package main.model;


public class Zutat
{
    String zutatenname;
    String menge;
    String einheit;
    

    //public String[] zutatformatieren(String namex,String menge,String einheit)
    

        @Override
    public String toString(){
        return menge + " " + einheit + " " + zutatenname + "\n";
    }






    public Zutat(String menge,String einheit,String zutatenname)
    {
        this.zutatenname = zutatenname;
        this.menge = menge;
        this.einheit = einheit;
    }
    
    public void anzeigen()
    {
        System.out.println(menge + "" + einheit + "" + zutatenname);
    }

    public String getName()
    {
        return zutatenname;
        }

        public String getMenge()
        {
            return menge;
        }

        public String getEinheit()
        {
            return einheit;
    }
}


