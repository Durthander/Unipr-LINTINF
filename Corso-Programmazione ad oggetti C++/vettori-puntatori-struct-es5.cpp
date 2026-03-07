//Si scriva un programma in cui data una matrice bidimensionale di valori (interi o float o double) individui 
//la colonna la cui somma degli elementi ha valore maggiore

#include <iostream>
#include <cstdlib>
#include <limits> // per poter usare INT_MIN ‐ vedi dopo 
const int NRIGHE=4;
const int NCOLONNE=3;
using namespace std;

int main() {
		int matrice[NRIGHE][NCOLONNE];
		int i, j, somma, massimo = INT_MIN, idmassimo=-1; // metto in massimo il valore più piccolo possibile di int 
			// in modo che qualunque valore sia maggiore di quello iniziale 
			
	    // leggo i valori della matrice 
		for (i = 0; i<NRIGHE; i++)
		{
		 cout << "Inserire gli elementi della riga " << i << endl;
		 for (j = 0; j<NCOLONNE; j++)
		 {
			cin >> matrice[i][j];
		 }
		}

		// stampo matrice
		cout << endl << "matrice inserita" << endl;
		for (i = 0; i<NRIGHE; i++)
		{
			for (j = 0; j<NCOLONNE; j++)
				cout << matrice[i][j] << " ";
			cout << endl;
		}

		for (i=0; i<NCOLONNE; i++)
		{
			somma = 0;
			for (j=0; j<NRIGHE; j++)
				somma += matrice[j][i];
			if (somma>massimo)
			{
				massimo = somma; idmassimo = i;
			}
		}
		cout << "Il valore massimo della somma dei valori e': " << massimo << endl;
		cout << "nella colonna: " << idmassimo << endl;
		return 0;
}