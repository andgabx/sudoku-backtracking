#ifndef GENERATOR_H
#define GENERATOR_H

#include "sudoku.h"

// LCG (Linear Congruential Generator)
void lcg_seed(unsigned int seed);
unsigned int lcg_next(void);

// Geração de Sudoku
bool fill_sudoku(Sudoku* sudoku, int row, int col);
Sudoku* generate_sudoku(int size, int empty_cells, unsigned int seed);

// Conversão para string
char num_to_char(int num);
void sudoku_to_string(Sudoku* sudoku, char* buffer, int buffer_size);

#endif

