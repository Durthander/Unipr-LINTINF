/*
In un esercizio di telepatia, un sensitivo scommette di essere in grado di indovinare almeno 3 numeri
consecutivi, in una sequenza di N numeri interi pensati da uno spettatore.Si scriva un programma che
crei un array di dimensione N, con allocazione dinamica, in cui il numero N e la sequenza di numeri pensati dallo spettatore vengono letti da tastiera, e verifichi se il sensitivo dice la verità.
Il programma acquisisce dal sensitivo i 3 numeri(con input da tastiera).
Il programma verifica, se esiste, nella sequenza di N numeri contenuti nell’array una sotto - sequenza di 3 numeri esattamente uguale a quella inserita dal sensitivo.
*/

#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

int main() {
	int N, i, j, trovato=1;
	int telepata[3];

	cout << "Spettatore: Inserire il valore N =";
		cin >> N;

	int *sequenza = new int[N];
	cout << "Leggo i numeri dallo spettatore" << endl;
	for (i = 0; i<N; i++) {
		cout << "Inserire il numero dello spettatore " << i+1 << "/" << N << ": ";
		cin >> sequenza[i];
	}

	cout << "Sequenza letta dallo spettatore" << endl;
	for (i = 0; i<N; i++) {
		cout << sequenza[i] << " ";
	}

	cout << endl << "Leggo i 3 elementi della sequenza:"<< endl;
	for (i = 0; i<3; i++)
	{
		cout << "Inserire il valore della sequenza del telepata "<< i+1 << "/3: ";
		cin >> telepata[i];
	}
	for (i = 0; i<N-2; i++)
	{
		trovato = 1;
		for (j = 0; j<3; j++)
			if (sequenza[i + j] != telepata[j])
		    {
			 trovato = 0; break;
		    } // esco dal ciclo for e passo al prossimo carattere della sequenza 
		if (trovato == 1) // vuol dire che sono arrivato qui senza il break quindi avendo trovato tutta la sequenza 
			break;
	}

	delete[] sequenza;

	if (trovato == 1)
		cout << "Incredibile!!! Il telepata ha indovinato!!!";
	else
		cout << "E' solo un buffone!!! Non ha indovinato!!!";
	return 0;
}