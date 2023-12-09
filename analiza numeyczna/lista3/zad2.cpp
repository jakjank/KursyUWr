#include <bits/stdc++.h>
#include <math.h>
using namespace std;

pair<double,double> pierw(double a,double b,double c){
    return make_pair((-b-sqrt(pow(b,2)-4.0*a*c))/(2.0*a),
                     (-b+sqrt(pow(b,2)-4.0*a*c))/(2.0*a));
}

pair<double,double> pierw_lepiej(double a,double b,double c){
    double x1,x2;
    if(b<0){
        x1 = (-b+sqrt(pow(b,2)-4.0*a*c))/(2.0*a);
    }
    else{
        x1 = (-b-sqrt(pow(b,2)-4.0*a*c))/(2.0*a);
    }
    x2 = c/(a*x1);
    return make_pair(x1,x2); 
}

int main(){
    //cout<<setprecision(40);
    double a,b,c;
    a = pow(10,-20);
    c = a;
    b = pow(10,15);
    pair<double,double> w = pierw(a,b,c);
    cout<<"x1: "<<w.first<<", x2: "<<w.second<<endl;
    cout<<"f(x1): "<<a*pow(w.first,2)+b*w.first+c<<", f(x2); "<<a*pow(w.second,2)+b*w.second+c<<endl<<endl;

    w = pierw_lepiej(a,b,c);
    cout<<"x1: "<<w.first<<", x2: "<<w.second<<endl;
    cout<<"f(x1): "<<a*pow(w.first,2)+b*w.first+c<<", f(x2); "<<a*pow(w.second,2)+b*w.second+c<<endl<<endl;
    return 0;
}