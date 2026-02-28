```java
import java.util.Random;
import java.util.Scanner;
import javax.swing.JFrame;

public class Main 
{
     //hier werden variablen generiert
    
    static Random rand = new Random();
    static int ratezahl = rand.nextInt(0,100);
    static int versuche = 0;

    public static void eingabe(){
        //versuche +1 immer wenn diese Funktion ausgeführt wird.
        versuche++;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Willkommen beim Zahlratespiel\n"+
        "Bitte geben sie eine Zahl ein!\n\n"+
        "Eingabe:");
        int eingabezahl = scanner.nextInt();
        raten(eingabezahl);
    }
    
    public static void openUI(){
        JFrame frame = new JFrame("Rate die Zahl");
        frame.setSize(800,600);
        frame.setLocation(100,150);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setDefaultLookAndFeelDecorated(true);

        frame.setVisible(true);
    }

    public static void raten(int eingabezahl){
        

        System.out.println(ratezahl);

        if (eingabezahl == ratezahl){
            System.out.println("Die gesuchte Zahl wurde erraten!.\n"+
                "Du hast " + versuche + " Versuche gebraucht!"
            );
        }else{
            if (eingabezahl > ratezahl){
                System.out.println("Die gesuchte Zahl ist kleiner.");
            }else{
                System.out.println("Die gesuchte Zahl ist größer");
            }
        } 
        
        

        eingabe();

    }

    public static void main(String[] args) {
    openUI();
    eingabe();
    

    }

    
    
}


``` 
