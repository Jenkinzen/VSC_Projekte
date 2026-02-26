import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;


public class Main 
{
     //hier werden variablen generiert
    
    static Random rand = new Random();
    static int ratezahl = rand.nextInt(0,100);
    static int versuche = 0;
    static JLabel text = new JLabel("Erraten sie die Zahl zwischen 1 und 100\n"+
            "Eingabe:");
    static JLabel counter = new JLabel("Versuche: "+ versuche);
            

    ////////////////////////////////////UI///////////////////////////////////////////////////

    public static void raten(int eingabezahl){
        
        versuche++;
        counter.setText("Versuche: " + versuche);

        System.out.println(ratezahl);

        if (eingabezahl == ratezahl){
            text.setText("Die gesuchte Zahl wurde erraten!.\n"+
                "Du hast " + versuche + " Versuche gebraucht!"
            );
        }else{
            
            if (eingabezahl > ratezahl){
                text.setText("Die gesuchte Zahl ist kleiner.");
            }else{
                text.setText("Die gesuchte Zahl ist größer");
            }
        } 
    }
    
    ///////////////////////////////////GUI////////////////////////////////////////////////
    
    public static void openUI(){
        JFrame frame = new JFrame("Rate die Zahl");
        frame.setSize(800,600);
        frame.setLocation(100,150);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setDefaultLookAndFeelDecorated(true);

            text.setBounds(300,100,200,50);

        JTextField textfield = new JTextField();
        textfield.setBounds(300,200,200,50);

        counter.setBounds(500,400,200,50);



        JButton button = new JButton("Raten!");
        button.setBounds(300,400,200,50);

        button.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e) {
                try{
                String textFromTextfield = textfield.getText();
                Integer eingabezahl = Integer.parseInt(textFromTextfield);
                raten(eingabezahl);
                }
                catch (Exception error)
                {
                    text.setText("Bitte eine Zahl eingeben!");
                }
            }
            

        });

        frame.add(text);
        frame.add(textfield);
        frame.add(button);
        frame.add(counter);
        frame.setLayout(null);
        frame.setVisible(true);

    }


    public static void main(String[] args) {

    openUI();
    

    }

    
    
}

