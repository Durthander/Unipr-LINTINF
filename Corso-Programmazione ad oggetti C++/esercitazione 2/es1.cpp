/*Scrivere un programma che definisca una classe Libro. La classe deve
contenere:
- 2 dati membro privati: titolo (stringa), pagine (numero int)
- Un costruttore che consenta di inizializzare i dati membro, e che contenga
anche dei valori di inizializzazione di default (stringa vuota per titolo, 0 per
numero di pagine)
- Metodi “set” e “get” per leggere e modificare ciascun dato membro
Scrivere nel “main” un codice di test che crei alcuni oggetti di tipo Libro,
modifichi alcuni dati membro e stampi i dati membro di ciascun oggetto.*/

#include <iostream>
#include <string>

using namespace std;
class Libro {
private:
  string titolo;
  int pagine;

public:
  Libro(string t = "", int p = 0) {
    titolo = t;
    pagine = p;
  }

  int getPagine() { return pagine; }

  string getTitolo() { return titolo; }

  void setPagine() {
    cout << "Quante pagine ha il libro? ";
    cin >> pagine;
  }

  void setTitolo() {
    cout << "Come si chiama il libro? ";
    cin >> titolo;
  }
};

int main(void) {
  Libro l1("Cane volante", 200);

  cout << "numero pagine = " << l1.getPagine() << " e il titolo è "
       << l1.getTitolo() << "." << endl;

  l1.setPagine();
  l1.setTitolo();

  cout << "nuove numero pagine = " << l1.getPagine() << " e il nuovo titolo è "
       << l1.getTitolo() << "." << endl;

  return 0;
}