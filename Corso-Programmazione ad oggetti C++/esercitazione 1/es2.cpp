/*Due colleghi intendono fissare una riunione, pertanto devono identificare dei giorni nei quali sono
entrambi liberi da impegni. A tale scopo, si realizzi un programma che permetta a ciascuno di
immettere i propri giorni di disponibilità da tastiera, e che identifichi tutti i giorni nei quali entrambi sono liberi. Il
programma deve chiedere i giorni di disponibilità ad entrambi i colleghi in successione (ciascuna persona può
inserire un numero arbitrario di giorni di disponibilità, utilizzare il valore 0 per indicare la fine della sequenza dei
giorni in cui ciascuna persona è libera da impegni).
Si consideri che la riunione sia nel mese corrente, quindi non interessa acquisire mese e anno, ma solo i giorni. Si
memorizzi la disponibilità di ciascuna persona in un array di interi positivi di 31 elementi in cui il valore 1
rappresenta un giorno disponibile e un valore 0 rappresenta un giorno impegnato.
E’ necessario verificare che i giorni siano numeri interi compresi tra 1 e 31.
Il programma deve alla fine visualizzare tutti i giorni in cui entrambe le persone sono libere da impegni.*/

#include <iostream>
using namespace std;

const int N = 31;

int main(void) {
    int p1[N], p2[N], i;

    for(i=0; i<N; i++) {
        p1[i] = 0;
        p2[i] = 0;
    }

    cout << "Inserire i giorni di disponibilita del primo collega (0 per terminare): ";
    cin >> i;
    while(i != 0) {
        if(i >= 1 && i <= N) {
            p1[i] = 1;
        }
        cin >> i;
    }

    cout << "Inserire i giorni di disponibilita del secondo collega (0 per terminare): ";
    cin >> i;
    while(i != 0) {
        if(i >= 1 && i <= N) {
            p2[i] = 1;
        }
        cin >> i;
    }

    cout << "Giorni in cui entrambi i colleghi sono liberi: ";
    for(i=1; i<=N; i++) {
        if(p1[i] == 1 && p2[i] == 1) {
            cout << i << " ";
        }
    }
    cout << endl;

    return 0;
}