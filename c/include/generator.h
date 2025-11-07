
#ifndef GENERATOR_H
#define GENERATOR_H

#include "sudoku.h"

// Gera um puzzle de Sudoku válido com um número específico de células vazias
Sudoku* generate_sudoku(int size, int empty_cells);

// Função auxiliar para preencher o Sudoku com solução válida
bool fill_sudoku(Sudoku* sudoku, int row, int col);

#endif // GENERATOR_H
