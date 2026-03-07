//Crivello di Eratostene. Stampa tutti i numeri primi compresi tra 1 e N.

#include <iostream>
using namespace std;

const int N = 10000;

int main()
{
	int i, a[N];
	for (i = 2; i < N; i++) a[i] = 1;
	for (i = 2; i < N; i++)
		if (a[i])
			//for (int j = i; j*i < N; j++) a[i*j] = 0;
		    for (int j = 2; j*i < N; j++) a[i*j] = 0;
	for (i = 2; i < N; i++)
		if (a[i]) cout << " " << i;
	cout << endl;
}