#include <bits/stdc++.h>
#include <math.h>
using namespace std;

int oblicz(double R,double x0){
    double x1 = x0*(2-x0*R);
    int licznik=1;

    while(x1+pow(10,-13) < 1.0/R or x1-pow(10,-13) > 1.0/R){
        //cout<<x1<<"   "<<1/R<<endl;
        x0 = x1;
        x1 = x0*(2.0-x0*R);
        licznik++;
    }
    return licznik;
}

int main(){
    cout<<setprecision(30);
    double suma=0;
    double ile=0;
    for(double i=0.01;i<100;i += 0.01){ //R
        for(double j=0.01;j<2.0/i;j += 0.01){ //x0
            // cout<<i/100.0<<"   "<<j/500.0<<endl;
            suma += oblicz(i,j);
            ile++;
        }
    }
    cout << "srednia liczba iteracji: "<<suma/ile;

    return 0;
}