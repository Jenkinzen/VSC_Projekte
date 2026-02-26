```java
public class Main {
        
    public static void main(String[] args) {
        
        //alter wird ergänzt, man muss nur die NR schreiben
        //(parameterreihenfolge wird befolgt wie bei python)
        vorstellung(31);
        vorstellung(21);



    }

    public static void vorstellung(Integer alter){
        //kein plan warum hier drunter das x: autocompleted wird
        System.out.println("asdasdasd");

        String name = "Gordon";
        
        //Integer alter = 31; wird jetzt durch den Parameter erzeugt

        String wohnort = "Bonn";

        String job = "arbeitslos";

        System.out.println("Moin, ich bin " + name +", "+ alter + 
        " Jahre alt, komme aus " + wohnort + " und bin momentan " + job);

        if(alter > 30){
            System.out.println("Ich bin über 30 Jahre alt");
        }else{
            System.out.println("Ich bin unter 30 Jahre alt");
        }
    }


}
```