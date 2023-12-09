#include <bits/stdc++.h>
#include <math.h>
using namespace std;

double met_newtona(double x0,double a){
    double x1,tmp;
    x1 = 1.5*x0 - 0.5*pow(x0,3)*a; 
    for(int i=0;i<25;i++){
        tmp = x1;
        x1 = 1.5*x0 - 0.5*pow(x0,3)*a;
        x0 = tmp;
        //cout<<x1<<endl;
    }
    return x1;
}

int main(){
    cout<<setprecision(10);
    cout<<"'miejsce zerowe x^2-1/sqrt(a)"<<endl;
    for(int i=0;i<100;i++){
        for(int j=1;j<100;j++){
            cout<<"x0 = "<<i/10.0<<", a = "<<j/10.0<<" : "<<met_newtona(i/10.0,j/10.0)<<endl;
            // w wiekszosci wychodzi zle
        }
    }
    //met_newtona(1,2);
    return 0;
}
