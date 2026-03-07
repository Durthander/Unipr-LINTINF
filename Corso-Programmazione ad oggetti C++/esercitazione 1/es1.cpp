/*Scrivere un programma che crei tre array di numeri interi a,b e c di lunghezza N=5. Il vettore b va inizializzato con
la sequenza di numeri 0, ‐3, 6, ‐9, 12 (in alternativa all’inserimento manuale, i numeri di b possono essere calcolati
con una formula). Il vettore a va creato con dei numeri a scelta. Il programma deve
calcolare la somma incrociata degli elementi: a[0]+b[N-1], a[1]+b[N-2], …, a[N-1]+b[0]
e memorizzarla nel vettore c. Il programma deve inoltre creare un vettore d della stessa lunghezza
con valore 1 se a[i] > b[i], 0 se a[i]=b[i] e ‐1 altrimenti. Si visualizzino i contenuti di a, b, c, d.*/

#include <iostream>
#include <cmath>

const int N = 5;

using namespace std;

int main(void) {
    int a[N] = {23, 0, 10, 12, 1};
    int b[N];
    int c[N];
    int d[N];
    int i;

    for(i=0; i < N; i++)
    {
        b[i] = pow(-1, i)*(i*3);
    }
    
    for(i=0; i < N; i++)
    {
        c[i] = a[i]+b[N-1-i];
    }
   
        for (i = 0; i < N; i++) {
        if (a[i] > b[i]) {
            d[i] = 1;
        } else if (a[i] < b[i]) {
            d[i] = -1;
        } else {
            d[i] = 0;
        }
    }

    
	cout << "Valori di a: ";
	for (i = 0; i<N; i++)
		cout << a[i] << " ";
	cout << endl << "Valori di b: ";
	for (i = 0; i<N; i++)
		cout << b[i] << " ";
	cout << endl << "Valori di c: ";
	for (i = 0; i<N; i++)
		cout << c[i] << " ";
	cout << endl << "Valori di d: ";
	for (i = 0; i<N; i++)
		cout << d[i] << " ";
	return 0;
}





