#include <bits/stdc++.h>
#include <math.h>
using namespace std;

double f(double x){
    return x-0.49;
}

void bisekcja(double a, double b){
    double m;
    double a0 = a, b0 = b;
    int n=0;
    while(n<=5){
        m = (a+b)/2.0;
        cout<<"["<<a<<", "<<b<<"]:  en = "<<0.49-m<<" <= "<<pow(2,-n-1)*(b0-a0)<<endl;

        if(f(a)*f(m)<0){
            b=m;
        }
        else{
            a=m;
        }
        n++;
    }
}


int main(){
    bisekcja(0,1);
    return 0;
}

//wyniki mowia, ze wartosc bledu niekoniecznie maleje razem z iloscia krokow :)