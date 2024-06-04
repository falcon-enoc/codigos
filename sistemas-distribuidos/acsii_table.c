#include<stdio.h>
//#include<.h>

int main(){
    char car;
    printf("Tabla ASCII truncada:\n");
    for(int i=48;(i>47 && i<127);i++){// tabla acsii truncada
        printf("caracter %c : numero ascii %d\n",i,i);
    }
    printf("Tabla ASCII completa:\n");
    for(int i=0;i<256;i++){// tabla acsii truncada
        printf("caracter %c : numero ascii %d\n",i,i);
    }
    printf("Escribe un caracter: ");
    scanf("%c",&car);

    // if((car > 96 && car < 123)||(car >= 65 && car <= 90))
    // printf("Es la letra %c con numero ascii %d\n",car, car);

    if((car > 'a' && car < 'z')||(car >= 'A' && car <= 'Z'))
    printf("Es la letra %c con numero ascii %d\n",car, car);
    else if ((car > '0' && car < '9'))
    {
        printf("Es la entero %c con numero ascii %d\n",car, car);
    }else{
        printf("No es letra ni numero, pajaron\n");
    }
    return 0;
}