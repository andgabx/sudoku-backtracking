
#include "../include/generator.h"
#include "../include/backtracking.h"
#include <stdlib.h>
#include <time.h>
#include <string.h>

// Função auxiliar para embaralhar um array
void shuffle(int* array, int n) {
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

// Preenche o Sudoku recursivamente com uma solução válida
bool fill_sudoku(Sudoku* sudoku, int row, int col) {
    if (row == sudoku->size) {
        return true;
    }
    
    int next_row = (col == sudoku->size - 1) ? row + 1 : row;
    int next_col = (col == sudoku->size - 1) ? 0 : col + 1;
    
    // Cria array com números embaralhados
    int* numbers = (int*)malloc(sudoku->size * sizeof(int));
    for (int i = 0; i < sudoku->size; i++) {
        numbers[i] = i + 1;
    }
    shuffle(numbers, sudoku->size);
    
    for (int i = 0; i < sudoku->size; i++) {
        int num = numbers[i];
        if (is_valid(sudoku, row, col, num)) {
            sudoku->grid[row][col] = num;
            if (fill_sudoku(sudoku, next_row, next_col)) {
                free(numbers);
                return true;
            }
            sudoku->grid[row][col] = 0;
        }
    }
    
    free(numbers);
    return false;
}

Sudoku* generate_sudoku(int size, int empty_cells) {
    srand(time(NULL));
    
    Sudoku* sudoku = sudoku_create(size);
    
    // Preenche o Sudoku com uma solução válida
    fill_sudoku(sudoku, 0, 0);
    
    // Remove células aleatoriamente
    int total_cells = size * size;
    int cells_to_remove = empty_cells;
    
    // Cria array de posições
    int* positions = (int*)malloc(total_cells * sizeof(int));
    for (int i = 0; i < total_cells; i++) {
        positions[i] = i;
    }
    shuffle(positions, total_cells);
    
    // Remove células
    for (int i = 0; i < cells_to_remove && i < total_cells; i++) {
        int pos = positions[i];
        int row = pos / size;
        int col = pos % size;
        sudoku->grid[row][col] = 0;
    }
    
    free(positions);
    
    return sudoku;
}
