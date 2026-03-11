/*Modificare la classe Persona dell’esercizio 2 aggiungendo un operatore binario “!=”
bool operator != (Persona p2)
come funzione membro, per determinare se due oggetti Persona sono diversi. Due oggetti Persona sono
diversi se almeno uno dei tre dati membro è diverso (nome, cognome, anni). Creare due oggetti Persona
nel “main” e creare un file “output.txt” (aperto in scrittura). Se i due oggetti Persona sono diversi
scrivere sul file la stringa “DIVERSI”, altrimenti scrivere nel file la stringa “UGUALI”.*/

#include <iostream>
#include <string>
#include <fstream>
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
    bool operator != (Persona p2) {
        if (nome != p2.nome || cognome != p2.cognome || anni != p2.anni)
            return true;
        else
            return false;
    }

};

int main(void) {
    Persona p1("Riccardo", "Rossi", 20), p2("Riccardo", "Rossi", 20);

    cout << "-- Persone Create --" << endl;
    cout << p1.getInformation() << endl;
    cout << p2.getInformation() << endl;
    ofstream file("output.txt");
    if (!file) {
        cerr << "Errore creazione file." << endl;
        return 1;
    }

    if (p1 != p2) {
        file << "DIVERSI" << endl;
        cout << "DIVERSI" << endl;
    } else {
        file << "UGUALI" << endl;
        cout << "UGUALI" << endl;
    }

    file.close();

    return 0;
}