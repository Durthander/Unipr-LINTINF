/*Scrivere un programma in cui dato il prezzo netto di un prodotto (variabile
float inserita in ingresso da tastiera) lo sconti del 35% se tale prezzo è > 100
e poi aggiunga l'IVA del 22% stampando a video il risultato finale.*/

#include <iostream>
using namespace std;

int main(void) {
  float p;
  float sconto = 0;

  cout << "Prezzo prodotto? ";
  cin >> p;

  if (p > 100) {
    sconto = p * 0.35;
  }

  float prezzo_scontato = p - sconto;
  float prezzo_finale = prezzo_scontato * 1.22; // aggiunge il 22% IVA

  cout << "Prezzo finale: " << prezzo_finale << endl;

  return 0;
}