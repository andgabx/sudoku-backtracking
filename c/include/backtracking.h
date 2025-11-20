#ifndef BACKTRACKING_H
#define BACKTRACKING_H

#include "sudoku.h"
#include <stdbool.h>

typedef struct {
    int row;
    int col;
} Coordenada;

typedef struct {
    double time_seconds;
    long long iterations;
    bool solved;
} SolveResult;

SolveResult solve_sudoku_iterative(Sudoku* sudoku);
bool is_in_row(Sudoku* sudoku, int r, int num);
bool is_in_col(Sudoku* sudoku, int c, int num);
bool is_in_box(Sudoku* sudoku, int r, int c, int num);
bool is_safe(Sudoku* sudoku, int r, int c, int num);
int find_all_empty_cells(Sudoku* sudoku, Coordenada lista_vazias[]);
int find_next_valid_number(Sudoku* sudoku, int r, int c, int num_inicio);

#endif 