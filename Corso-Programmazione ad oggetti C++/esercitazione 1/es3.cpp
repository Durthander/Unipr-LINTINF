/*E’ noto che esiste una definizione matematica della radice quadrata che si basa sulla seguente sequenza
numerica: 𝑥1 = 1, 𝑥(𝑛+1) = 0,5(𝑥𝑛 + 𝑎/𝑥𝑛) dove a è un numero reale positivo.
Si può dimostrare che: lim𝑖→∞(𝑥𝑖) = √𝑎
Si scriva un programma in cui si calcola la radice quadrata di tre numeri memorizzati in un array.
Il ciclo di calcolo della radice può fermarsi per esempio dopo 100 cicli oppure quando la differenza in valore
assoluto tra il valore effettivo della radice (sqrt(a)) e xn+1 diventa inferiore ad un valore di soglia (es:
0.001). Utilizzare la funzione abs() per calcolare la differenza in valore assoluto.*/

#include <cmath>
#include <iostream>
using namespace std;

int main(void) {
    int numeri[3]= {20, 43, 2};


    for (int i = 0; i<3; i++)
    {
        int a = numeri[i];
        float x_n = 1;
        float x_n1;

        for(int j=0; j<1000000; j++)
        {
            x_n1 = 0.5 * (x_n + a / x_n);

            if(abs(sqrt(a) - x_n1) < 0.001) {
                break;
            }

            x_n = x_n1;
        }

        cout << "La radice di " << numeri[i] << " è " << x_n1 << endl;

    }
   return 0;
} 