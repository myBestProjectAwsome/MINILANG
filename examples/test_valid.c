#include <stdio.h>
#include <stdlib.h>

int main() {
    int x = 42;
    int y = (x + 10);
    printf("%d\n", y);
    if ((y > 50)) {
        printf("%d\n", 1);
    } else {
        printf("%d\n", 0);
    }
    return 0;
}