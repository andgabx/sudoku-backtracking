
#ifndef SUDOKU_H
#define SUDOKU_H

#include <stdbool.h>

// Estrutura para representar um Sudoku
typedef struct {
    int** grid;
    int size;      // Tamanho do grid (3, 6 ou 9)
    int box_size;  // Tamanho da caixa (sqrt(size): 1 para 3x3, 2 para 6x6, 3 para 9x9)
} Sudoku;

// Funções de criação e destruição
Sudoku* sudoku_create(int size);
void sudoku_destroy(Sudoku* sudoku);

// Funções de validação
bool is_valid(Sudoku* sudoku, int row, int col, int num);

// Funções auxiliares
void sudoku_copy(Sudoku* dest, Sudoku* src);
void sudoku_print(Sudoku* sudoku);
int count_empty_cells(Sudoku* sudoku);

#endif // SUDOKU_H
