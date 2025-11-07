
#ifndef BACKTRACKING_H
#define BACKTRACKING_H

#include "sudoku.h"
#include <stdbool.h>

// Estrutura para armazenar as coordenadas de uma célula
typedef struct {
    int row;
    int col;
} Coordenada;

// Estrutura para armazenar resultados
typedef struct {
    double time_seconds;
    long long iterations;
    bool solved;
} SolveResult;

// Função principal de backtracking iterativo
SolveResult solve_sudoku_iterativo(Sudoku* sudoku);

#endif // BACKTRACKING_H
