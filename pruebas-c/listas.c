#include <stdio.h>
#define n 10000

int arreglo[n];

int main(){

    for(int i=0;i<n;i++){

        arreglo[i]=i+1;
        printf("%d\n", arreglo[i]);
    }


    return 0;
}