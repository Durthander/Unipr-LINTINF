//Ricerca dicotomica di un elemento in un array di numeri interi ordinato in modo crescente.

#include <iostream>
using namespace std;
const int N = 11;

int search(int a[], int v, int l, int r)
{
	while (r >= l)
	{
		int m = (l + r) / 2;
		if (v == a[m]) return m;
		if (v < a[m]) r = m - 1; else l = m + 1;
	}
	return -1;
}

int main()
{
	int result,value;
	int array[N]= {3,5,7,9,15,22,46,98,111,200,301};
	
	value = 10;
	result=search(array,value,0,N-1);
	if (result>=0)
		cout << value << " trovato" << endl;
	else
		cout << value << " non trovato" << endl;

	value = 22;
	result=search(array,value, 0, N-1);
	if (result>=0)
		cout << value << " trovato" << endl;
	else
		cout << value << " non trovato" << endl;
}