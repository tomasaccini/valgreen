#include <stdio.h>
#include <stdlib.h>

/* 
Compilacion:
    gcc -g errores_tipicos.c -o errores
        * g: Compila con información de debugging, para que programas como Valgrind y GDB vean bien donde estan los errores, entre otras cosas.
Corrida:
    ./errores
Chequeo de perdida de memoria:
    valgrind  --leak-check=full --track-origins=yes --show-reachable=yes ./errores
        * leak check full: Mostrar en detalle cada perdida, en vez de un resumen
        * track origins yes: Mostrar donde se originaron los valores no inicializados (ejemplo en no_inicializar())
        * show reachable yes: Para mostrar todo tipo de memory leaks, incluso los que al terminar la ejecucion el sistema operativo se encarga de arreglar. Estos también hay que corregirlos
*/

void no_liberar() {
    /* Todo malloc debe ser liberado. De lo contario, se pierde la referencia a la memoria.
    Produce un memory leak (definitely lost) de 100 bytes. */
    int* arreglo = malloc(100);
}

void no_inicializar() {
    /* Todas las variables (estáticas o dinámicas) deben tener un valor asignado. Si no, se almacena basura en ellas.
    Produce el error conditional jump depends on uninitialized value, ya que un if depende de lo que hay dentro de la variable. */
    int x;
    if(x) printf(".");
    int* y = malloc(10);
    if(y[0]) printf(".");
    free(y);
}

void pisar_memoria(){
    /* Nunca hay que perder la referencia a la memoria. Si yo piso el valor de un puntero a memoria con otro valor, no tengo forma de recuperarlo.
    Produce un memory leak (definitely lost) de 100 bytes. */
    int* arreglo = malloc(100);
    arreglo = malloc(20);
    free(arreglo); //Solo libera los 20 bytes asignados la segunda vez. Los primeros 100 estan perdidos 
}

void escritura_error(){
    /* Siempre se debe tener en claro cuanta memoria es pedida. Puedo pedir memoria de más si no estoy seguro de cuanto usar (nunca con exceso, obviamente), pero nunca puedo acceder memoria mas alla de la pedida, ni para escribir ni para leer.
    Produce el error invalid write of size 1, porque se intenta acceder al tercer byte de un arreglo, pero solo se pidieron dos. */
    char* cadena_dinamica = malloc(2 * sizeof(char));
    cadena_dinamica[0] = 'A';
    cadena_dinamica[1] = 'B';
    cadena_dinamica[2] = 'C';
    free(cadena_dinamica);
}

void lectura_error(){
    /* Similar a invalid write, no se puede pedir el valor de un puntero de memoria pasada la memoria pedida. 
    Produce el error invalid read of size 1, por intentar leer 1 byte inexistente.
    Notese que Valgrind nos da una ayuda con qué se intento acceder. 'Adress is 3 bytes after a block of 2 bytes allocated', es decir, se intento acceder 3 bytes pasados los 2 pedidos, en este caso, la 5ta posición de un arreglo de 2 bytes. */
    char* cadena_dinamica = malloc(2 * sizeof(char));
    char x = cadena_dinamica[5];
    free(cadena_dinamica);
}

void liberar_multiples_veces(){
    /* La memoria pedida debe ser liberada solo una vez
    Produce invalid free, por intentar liberar multiples veces */
    int* arreglo = malloc(10);
    free(arreglo);
    free(arreglo);
}

int main() {
    no_liberar();
    pisar_memoria();
    escritura_error();
    lectura_error();
    no_inicializar();
    liberar_multiples_veces();
    return 0;
}
