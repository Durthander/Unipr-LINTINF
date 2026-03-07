//Scrivere un programma che legga N valori float in un array e stampi a 
//video valore massimo, minimo, il valore medio e la deviazione standard

#include <iostream>
#include <cstdlib>
const int N=4;

using namespace std;

int main(void)
{
	float v[N], massimo, minimo, media, devstd=0.0;
	int i;
	// leggo gli N valori float e li metto nel vettore v 
	for (i = 0; i<N; i++)
	{
		cout << "Inserisci un valore float " << i << " di " << N << ":";
		cin >> v[i];
	}
	// calcolo il valore massimo, minimo e media in un solo ciclo for. Avrei anche potuto farne 3 separati 
	minimo = massimo = media = v[0];
	for (i = 1; i<N; i++)
	{
		if (v[i]>massimo)
			massimo = v[i];
		if (v[i]<minimo)
			minimo = v[i];
		media += v[i];
	}
	media = media / N;
	for (i = 0; i<N; i++)
	{
		devstd += (v[i] - media)*(v[i] - media);
	}
	devstd = sqrt(devstd / N);
	cout << endl << "Il valore massimo e' " << massimo << endl;
	cout << endl << "Il valore minimo e' " << minimo << endl;
	cout << endl << "Il valore medio e' " << media << endl;
	cout << endl << "La deviazione standard e' " << devstd << endl;
	return 0;
}
