#ifndef GENERATOR_H
#define GENERATOR_H

#include "sudoku.h"

Sudoku* generate_sudoku(int size, int empty_cells);
bool fill_sudoku(Sudoku* sudoku, int row, int col);

#endif 
