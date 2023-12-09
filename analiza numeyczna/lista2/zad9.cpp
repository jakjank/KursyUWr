#include <iostream>
#include <math.h>

using namespace std;

double pi1(int n){
    if(n==1){
        return 2.0;
    }
    return pow(2,n-1) * sqrt(2*(1-sqrt(1 - pow(pi1(n-1) / pow(2,n-1),2))));   
}

double pi2(int n){
    if(n==1){
        return 2.0;
    }
    return sqrt(pow(2,2*n-1) - pow(2,n) * pi2(n-1) * sqrt(pow(2,2*n-2) / pow(pi2(n-1),2) - 1));
}

int main(){
    cout.precision(15);
    cout << M_PI << " - poprawna wartosc pi" << endl;
    cout << pi1(15) << " - pi1 dla 15" << endl;
    cout << pi1(30) << " - pi1 dla 25" << endl << endl;

    cout << pi2(25) ;
    // widac ze mamy utrate cyfr znaczacych 
    return 0;
}