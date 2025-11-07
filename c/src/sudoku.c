
#include "../include/sudoku.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

Sudoku* sudoku_create(int size) {
    Sudoku* sudoku = (Sudoku*)malloc(sizeof(Sudoku));
    sudoku->size = size;
    sudoku->box_size = (int)sqrt(size);
    
    sudoku->grid = (int**)malloc(size * sizeof(int*));
    for (int i = 0; i < size; i++) {
        sudoku->grid[i] = (int*)calloc(size, sizeof(int));
    }
    
    return sudoku;
}

void sudoku_destroy(Sudoku* sudoku) {
    if (sudoku) {
        for (int i = 0; i < sudoku->size; i++) {
            free(sudoku->grid[i]);
        }
        free(sudoku->grid);
        free(sudoku);
    }
}

bool is_valid(Sudoku* sudoku, int row, int col, int num) {
    // Verifica linha
    for (int x = 0; x < sudoku->size; x++) {
        if (sudoku->grid[row][x] == num) {
            return false;
        }
    }
    
    // Verifica coluna
    for (int x = 0; x < sudoku->size; x++) {
        if (sudoku->grid[x][col] == num) {
            return false;
        }
    }
    
    // Verifica caixa
    int box_start_row = row - row % sudoku->box_size;
    int box_start_col = col - col % sudoku->box_size;
    
    for (int i = 0; i < sudoku->box_size; i++) {
        for (int j = 0; j < sudoku->box_size; j++) {
            if (sudoku->grid[box_start_row + i][box_start_col + j] == num) {
                return false;
            }
        }
    }
    
    return true;
}

void sudoku_copy(Sudoku* dest, Sudoku* src) {
    for (int i = 0; i < src->size; i++) {
        for (int j = 0; j < src->size; j++) {
            dest->grid[i][j] = src->grid[i][j];
        }
    }
}

void sudoku_print(Sudoku* sudoku) {
    for (int i = 0; i < sudoku->size; i++) {
        if (i % sudoku->box_size == 0 && i != 0) {
            for (int k = 0; k < sudoku->size * 2 + sudoku->box_size - 1; k++) {
                printf("-");
            }
            printf("\n");
        }
        
        for (int j = 0; j < sudoku->size; j++) {
            if (j % sudoku->box_size == 0 && j != 0) {
                printf("| ");
            }
            printf("%d ", sudoku->grid[i][j]);
        }
        printf("\n");
    }
}

int count_empty_cells(Sudoku* sudoku) {
    int count = 0;
    for (int i = 0; i < sudoku->size; i++) {
        for (int j = 0; j < sudoku->size; j++) {
            if (sudoku->grid[i][j] == 0) {
                count++;
            }
        }
    }
    return count;
}
