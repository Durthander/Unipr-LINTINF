//Scrivere un programma che, data una stringa di N caratteri, conti il numero di vocali 
//nella stringa e scriva tale valore sullo schermo.
//Si supponga che la stringa contenga soltanto caratteri minuscoli.
//Il programma deve inoltre stampare il massimo  carattere e la sua posizione 
//all’interno della stringa.
//Stampare a video anche la stringa invertita.
//Costruire una nuova frase in cui il primo carattere di ciascuna parola nella frase di partenza è stato 
//reso maiuscolo.Tutti gli altri caratteri devono essere resi minuscoli.


#include <iostream>
#include <string> 
#include <cstdlib>
#include <sstream>
using namespace std;

int main() {
		string s,invs;
		int conta = 0, maxid=0;
		char maxchar,c;
		cout << "Inserire una stringa: " << endl;
		getline(cin,s);
		maxchar = s[0];
		invs = s;

		for (int i=0; i<s.length(); i++)
		{
			if (s[i] == 'a' || s[i] == 'e' || s[i] == 'i' || s[i] == 'o' || s[i] == 'u')
				conta++;
			if (s[i]>maxchar)
			{
			 maxchar = s[i];
			 maxid = i;
			}
		}
		for (int i = 0, j = s.length()-1; i<j; i++, j--)
		{
			c = invs[i];
			invs[i] = invs[j];
			invs[j] = c;
		}
		cout << "La stringa "<< s << " contiene " << conta << " vocali" << endl;
		cout << "Il massimo carattere e' " << maxchar << " in posizione " << maxid << endl;
		cout << "la stringa invertita e' " << invs << endl;
		cout << "la stringa modificata e': ";
		istringstream str(s);
		string word;
		while (str >> word)
		{
			word[0]=toupper(word[0]);
			for (int i = 1; i < word.length(); i++)
				word[i]=tolower(word[i]);
			cout << word << " ";
		}
		return 0;
}