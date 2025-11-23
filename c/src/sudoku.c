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

Sudoku* sudoku_parse_from_string(const char* str, int size) {
    Sudoku* sudoku = sudoku_create(size);
    
    // Copia a string para poder usar strtok
    char* str_copy = (char*)malloc(strlen(str) + 1);
    strcpy(str_copy, str);
    
    char* line = strtok(str_copy, "\n");
    int row = 0;
    
    while (line != NULL && row < size) {
        // Pula linhas de separador (que começam com -)
        if (line[0] == '-') {
            line = strtok(NULL, "\n");
            continue;
        }
        
        // Parse números da linha, ignorando | e espaços
        int col = 0;
        for (int i = 0; line[i] != '\0' && col < size; i++) {
            // Se é um dígito, converte
            if (line[i] >= '0' && line[i] <= '9') {
                sudoku->grid[row][col] = line[i] - '0';
                col++;
                // Pula o resto do número se houver (não deve acontecer para Sudoku 3x3, 6x6, 9x9)
                while (line[i + 1] >= '0' && line[i + 1] <= '9') {
                    i++;
                }
            }
        }
        
        if (col > 0) {  // Só incrementa row se encontrou números
            row++;
        }
        line = strtok(NULL, "\n");
    }
    
    free(str_copy);
    return sudoku;
}
