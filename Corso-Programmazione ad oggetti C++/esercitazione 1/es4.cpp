/*Definire una struct “tipolibro” con gli attributi: titolo (string), autore (string), anno di edizione (int) e prezzo (int),
dove “titolo” e “autore” sono stringhe senza spazi. Scrivere un programma che legga da tastiera i dati di N
(costante definita nel programma) libri memorizzandoli in un array di strutture tipolibro. Il prezzo di ciascun libro
deve essere generato in modo casuale tra 0 e 200 all'interno del programma (per generare un numero casuale
intero compreso tra 0 e n-1 si utilizzi l’espressione rand()%n). 

Il programma deve quindi calcolare il prezzo medio
dei libri inseriti, determinare il libro con prezzo maggiore e il libro con l'anno di edizione più vecchio.*/


#include <iostream>
#include <string>
using namespace std;
const int N =3;
struct tipolibro {
    string titolo, autore;
    int anno_edizione, prezzo;

};

int main(void) {
    tipolibro l[3];

    for (int i =0; i < N; i++){
        
        cout << "Libro" << i + 1 << endl <<"Titolo: ";
        cin >> l[i].titolo;
        cout << "Autore: ";
        cin >> l[i].autore;
        cout << "Anno di edizione: ";
        cin >> l[i].anno_edizione;
        
        int n = 200;
        l[i].prezzo = rand()%n;
    }

   float somma = 0;
int maxp = l[0].prezzo;
int maxa = l[0].anno_edizione;
string n_maxp = l[0].autore;
string n_maxa = l[0].autore;

for (int i = 0; i < N; i++) {
    somma += l[i].prezzo;

    if (l[i].prezzo > maxp) {
        maxp = l[i].prezzo;
        n_maxp = l[i].autore;
    }

    if (l[i].anno_edizione < maxa) {
        maxa = l[i].anno_edizione;
        n_maxa = l[i].autore;
    }
}

float media = somma / N;
cout << "La media è " << media
     << ", il prezzo più alto è di " << n_maxp << " con " << maxp << "€"
     << ", il libro più vecchio è " << n_maxa << " dell'anno " << maxa << ".";

    return 0;

}