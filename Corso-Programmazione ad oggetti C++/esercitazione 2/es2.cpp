/*Scrivere un programma che definisca una classe Persona. La classe deve contenere:
 3 dati membro privati: nome (stringa), cognome (stringa), anni (numero intero)
 Un costruttore che consenta di inizializzare i dati membro
 Un metodo pubblico “string getInformation();” per ritornare le informazioni di una
persona nel formato: <prima lettera del nome>. <cognome>, <anni>
(esempio: “M. Rossi, 37”). Per estrarre il primo carattere di una variabile string s, in
formato string, è possibile utilizzare il metodo s.substr(0, 1)
 Un metodo pubblico “void setcognome(string c)” per modificare il cognome di una
persona con un valore passato come argomento
Creare nel “main” tre oggetti Persona con valori a scelta e stampare le informazioni di ciascuna persona
utilizzando il metodo “getInformation()”. Creare un array di 3 persone e salvare nell’array i tre oggetti
creati precedentemente. Scrivere un algoritmo (utilizzando un ciclo “for”) per modificare il cognome di
tutte le persone contenute nell’array con il valore “Bianchi” e stampare le informazioni di ciascuna
persona dopo la modifica del cognome.*/

#include <iostream>
#include <string>
using namespace std;

class Persona {
    private:
    string nome, cognome;
    int anni;

    public:
    Persona(string n = "", string c = "", int a = 0) {
        nome = n;
        cognome = c;
        anni = a;
    }

    string getInformation() {
        string p_lnome = nome.substr(0, 1);
        string s = p_lnome + ". " + cognome + ", " + to_string(anni);
        return s;
     }
    
    void setcognome(string c) {
        cognome = c;
    }

};

int main(void) {
    Persona p1("Mario", "Rossi", 37), p2("Riccardo", "Nezzi", 20), p3("Sebastiano", "Gandini", 25);

    cout << "-- Persone Create --" << endl;
    cout << p1.getInformation() << endl;
    cout << p2.getInformation() << endl;
    cout << p3.getInformation() << endl;

    Persona p[3] = {p1, p2, p3};

    cout << "\n-- Dopo l'aggiornamento a 'Bianchi' --" << endl;
    for(int i = 0; i < 3; i++) {
        p[i].setcognome("Bianchi");
        cout << p[i].getInformation() << endl;
    }

    return 0;
}