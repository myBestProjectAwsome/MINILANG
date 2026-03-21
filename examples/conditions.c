#include <stdio.h>
#include <stdlib.h>

int main() {
    int x = 42;
    if ((x > 10)) {
        printf("%d\n", 1);
    } else {
        printf("%d\n", 0);
    }
    int y = 5;
    if ((y > 10)) {
        printf("%d\n", 100);
    } else {
        printf("%d\n", 200);
    }
    return 0;
}