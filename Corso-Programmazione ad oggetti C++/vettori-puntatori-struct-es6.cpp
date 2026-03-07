//Conteggio del numero coppie di punti (x,y) a distanza inferiore ad una certa soglia. I punti vengono salvati in un array di strutture dati. 
//Le coordinate dei punti sono generate casualmente.

#include <math.h>
#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

struct point { float x; float y; };

float distance(point a, point b)
{
	float dx = a.x - b.x, dy = a.y - b.y;
	return sqrt(dx*dx + dy*dy);
}

float randFloat()
{
	return (float)rand() / RAND_MAX; // rand ritorna un numero in tero compreso tra 0 e RAND_MAX
}

int main(int argc, char *argv[])
{
	if (argc == 3)
	{
		srand(time(NULL)); //inizializza il seme dell'algoritmo di generazione di numeri casuali, va chiamato all'inizio del programma
		float d = atof(argv[2]);
		int i, cnt = 0, N = atoi(argv[1]);
		point *a = new point[N];
		for (i = 0; i < N; i++)
		{
			a[i].x = randFloat(); a[i].y = randFloat();
		}
		for (i = 0; i < N; i++)
			for (int j = i + 1; j < N; j++)
				if (distance(a[i], a[j]) < d) cnt++;
		cout << cnt << " pairs within " << d << endl;
	}
	else
	{
		cout << "errore nel numero di parametri, eseguire il programma con la seguente sintassi:" << endl;
		cout << "<nomeprogramma> <numero di punti> <soglia di distanza>";
    }
}