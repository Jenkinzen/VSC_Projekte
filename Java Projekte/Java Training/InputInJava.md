```java
import java.util.Scanner;
//muss importiert werden für inputs, nicht integriert wie bei python

public class Main {
      //funktionen können vor und nach public static void main 
      //definiert werden
    public static void dollarconverter(Double euro){
        System.out.println("Der Betrag ist " + euro * 1.20 + "Dollar");
    }

    public static void main(String[] args) {
        //1.Scanner ruft die Klasse auf die importiert wurde
        //2.scanner ist die selbst definierte variable ( könnte auch input heißen)
        //= new Scanner erzeugt ein neues Objekt der Klasse
        // System.in umschreibt den Eingabestrom des Systems , also die Tastatur-Eingabe.
        Scanner scanner = new Scanner(System.in);
        //sagt dem User nur was er Eingeben soll als print
        System.out.println("Bitte gebe einen Betrag in Euro ein");
        //die Zeile hier drunter ist quasi die Input funktion nur ohne integrierte Möglichkeit
        //was dabei zu schreiben, deshalb anstatt print , println + DatenTyp(Double) + variable = scanner.nextDateityp();
        //next -> die nächste Eingabe der Tastatur nachdem die Zeile ausgeführt wurde.
        Double money = scanner.nextDouble();
        dollarconverter(money);
        yenconverter(money);




    



    }
      //funktionen können vor und nach public static void main 
      //definiert werden
    public static void yenconverter(Double euro){
        System.out.println("Der Betrag ist " + euro * 183.00 + "Yen");
    }


}
```