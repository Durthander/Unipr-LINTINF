/*Scrivere un programma che legga da tastiera il raggio (variabile float) di un cerchio e ne stampi l'area. Utilizzare
una funzione con passaggio per riferimento dell’area.*/

#include <cmath>
#include <iostream>
using namespace std;

float AreaCerchio(float r)
{
    return 2*M_PI*pow(r,2);
}

int main(void) {
    float r;

    cout << "Raggio? ";
    cin >> r;
    float Area = AreaCerchio(r);

    cout << "L'area del cerhio è " << Area << ".";
    return 0;
}