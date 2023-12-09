#include <iostream>
#include <math.h>
using namespace std;

double f1_zle(double x){
    return 1 / (pow(x,3)+sqrt(pow(x,6)+pow(2023,2)));
}
double f1_lepiej(double x){
    if(x>=0){
        return 1 / (pow(x,3)+sqrt(pow(x,6)+pow(2023,2))); //zwracamy to samo bo jest OK
    }
    return (pow(x,3)-sqrt(pow(x,6)+pow(2023,2)))/pow(2023,2);
}

double f2_zle(double x){
    return log2(x)-2;
}
double f2_lepiej(double x){
    return log2(x/4);
}

double f3_zle(double x){ 
    return (M_PI_2 - x - (M_PI_2 - atan(x)))/pow(x,3);
}

// double f3_lepiej(double x){
//     if(abs(x)<=0.1){
//         double blad = pow(x,4)/(4), s_szer=x; 
//         int i=1;
//         while(blad > pow(10,-15)){
//             s_szer += pow(-1,i)*pow(x,2*i)/(2*i+1); //ale bedziemy wyciagac x dlatego bez +1 w odp miejscach
//             blad = pow(-1,i+1)*pow(x,2*i+2)/(2*i+3);
//             i++;
//             //cout<<blad<<endl;
//         }
//         return (s_szer-1)/pow(x,2);
//     }
//     return f3_zle(x);
// }

double f3_lepiej2(double x){
    return (-1)/pow(x,2)+atan(x)/pow(x,3);
}

int main(){
    cout<<f1_zle(-1000000)<<endl<<f1_lepiej(-1000000)<<endl<<endl;

    cout<<f2_zle(4+pow(10,-10))<<endl<<f2_lepiej(4+pow(10,-10))<<endl<<endl;

    cout<<f3_zle(0.000001)<<endl<<f3_lepiej2(0.000001);
    return 0;
}