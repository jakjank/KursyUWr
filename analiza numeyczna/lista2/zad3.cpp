#include <iostream>
#include <set>

using namespace std;

int main(){

    set<string> wyniki;
    int licz,mian;

    for(int mianownik=2; mianownik<33; mianownik*=2){
        for(int licznik=1; licznik<mianownik; licznik++){
            licz = licznik;
            mian = mianownik;
            while(licz%2 == 0 && mian%2 == 0){
                licz/=2;
                mian/=2;
            }
            wyniki.insert("0 " + to_string(licz) + "/" + to_string(mian));

            licz = 2*licznik;
            mian = mianownik;
            while(licz%2 == 0 && mian%2 == 0){
                licz/=2;
                mian/=2;
            }
            if(2*licznik >= mianownik){
                wyniki.insert("1 " + to_string(licz-mian) + "/" + to_string(mian));
            }
            else{
                wyniki.insert("0 " + to_string(licz) + "/" + to_string(mian));
            }
            licz = licznik;
            mian = 2*mianownik;
            while(licz%2 == 0 && mian%2 == 0){
                licz/=2;
                mian/=2;
            }
            wyniki.insert("0 " + to_string(licz) + "/" + to_string(mian));

        }
    }

    for(set<string>::iterator i = wyniki.begin(); i != wyniki.end(); i++){
        cout << *i << endl;
    }
    return 0;
}

// najmniejszy przedzial to [ -1.1111, +1,1111] = [ -1 15/16, 1 15/16]