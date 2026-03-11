/*Scrivere un programma che definisca due classi: Money e CreditCard. La classe Money deve contenere
due dati membri privati interi (euros e cents). La classe Money deve anche contenere:
 Costruttore che inizializza a 0 entrambi i dati membri.
 metodi pubblici per impostare e leggere il valori dei dati membri: get_euros(), set_euros(int e),
get_cents(), set_cents(int c)
 Un operatore ‘+’ definito come funzione non-membro: Money operator+(Money m1, Money m2)
che esegue la somma di due oggetti Money sommando euro e centesimi (i centesimi se
eccedono il valore di 100 vanno convertiti in euro: es 10.50 euro+ 5.70 euro= 16.20 euro)
 Un operatore ‘<<’ definito come funzione non-membro: ostream& operator<<(ostream& os,
Money m) per stampare a video i dati membri euros e cents */


#include <iostream>
#include <ostream>
#include <fstream>
#include <string>  
using namespace std;

class Money {
    private:
    int euros, cents;

    public:
    Money (int e = 0, int c = 0){
        euros = e;
        cents = c;
    }
    int get_euros() {return euros; }
    int get_cents() { return cents; }

    void set_euros(int e) { euros = e; }

    void set_cents(int c) { cents = c; }

};

Money operator+(Money m1, Money m2) {
    int total_cents = m1.get_cents() + m2.get_cents();
    int extra_euros = total_cents / 100;
    total_cents = total_cents % 100;

    int total_euros = m1.get_euros() + m2.get_euros() + extra_euros;

    return Money(total_euros, total_cents);
}

ostream& operator<<(ostream& os,
Money m){ 
    os << "€"<<m.get_euros()<<" e "<<m.get_cents()<< " centesimi";
    return os;
}

/*La classe CreditCard contiene tre dati membri privati: il nome del proprietario (string), il numero della
carta di credito (string), il totale dei pagamenti effettuati (oggetto della classe Money). La classe
CreditCard contiene anche:
 Costruttore per creare una carta dato il nome del proprietario e il numero della carta.
 Una funzione membro: print() per stampare il nome del proprietario e il numero
 Una funzione membro: Money get_totalcharges() che restituisce il totale dei pagamenti
 Una funzione membro: charge(string item, int e, int c) che aggiorna il totale dei
pagamenti a seguito di una singola spesa (con causale “item”) di euro ‘e’ e di centesimi ‘c’
Il programma principale crea un oggetto di tipo CreditCard, legge da un file di testo un elenco di spese e
aggiorna il totale dei pagamenti. Il file di testo delle spese contiene per ogni riga le informazioni di una
singola spesa su tre colonne: <causale della spesa> <euro> <centesimi>
es:
book 90 60
pizza 20 50*/
class CreditCard {
    private:
    string pnome, ncard;
    Money pdone;
    
    public:
    CreditCard (string p = "", string n = "", Money pd = Money(0,0)) {
        pnome = p;
        ncard = n;
        pdone = pd;
    }

    void print() {cout << "Nome proprietario carta: " << pnome << endl <<
        "numero carta: "<< ncard;}
    
    Money get_totalcharges() {return pdone;}

    void charge(string item, int e, int c) {
        Money spesa(e, c);
        pdone = pdone + spesa;
        cout << "Spesa per " << item << " di " << spesa << endl;
    }
};

int main(void) {
    CreditCard c1("Jacopo Aleotti", "000002992001999", Money(2,0));
    
    ifstream file("spese.txt");

    string item;
    int e, c;
    while (file >> item >> e >> c) {
        c1.charge(item, e, c);
    }
    file.close();

    cout << "\n--- Riepilogo Carta ---" << endl;
    c1.print();
    cout << "\nTotale addebiti: " << c1.get_totalcharges() << "\n-----------------------" << endl;

    return 0;
}