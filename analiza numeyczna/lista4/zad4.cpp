#include <bits/stdc++.h>
#include <math.h>
using namespace std;

double f(double x){
    if(x>-4) return pow(x,4) - log(x+4);
    return pow(x,4); 
}

void bisekcja(double a, double b){
    double m;
    double a0 = a, b0 = b;
    int n=floor(log2((b0-a0)/(2.0*pow(10,-8))))+1;
    //cout<<"n = "<<n<<endl;

    for(int i=0;i<n;i++){
        m = (a+b)/2.0;
        //cout<<m<<" - "<<b-a<<endl;
        if(f(a)*f(m)<0){
            b=m;
        }
        else{
            a=m;
        }
    }
    m = (a+b)/2;
    cout<<m<<endl;
}


int main(){
    cout<<setprecision(10);
    bisekcja(-2,0);
    bisekcja(0,3);
    return 0;
}

