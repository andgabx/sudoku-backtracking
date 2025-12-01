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

static char num_to_char(int num) {
    if (num == 0) {
        return '0';
    } else if (num >= 1 && num <= 9) {
        return '0' + num;
    } else if (num >= 10 && num <= 16) {
        return 'A' + (num - 10);
    } else {
        return '?';
    }
}

static int char_to_num(char c) {
    if (c == '0') {
        return 0;
    } else if (c >= '1' && c <= '9') {
        return c - '0';
    } else if (c >= 'A' && c <= 'G') {
        return c - 'A' + 10;
    } else if (c >= 'a' && c <= 'g') {
        return c - 'a' + 10;
    } else {
        return 0;
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
            printf("%c ", num_to_char(sudoku->grid[i][j]));
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
    
    // Create a copy of the string to modify safely
    char* str_copy = (char*)malloc(strlen(str) + 1);
    strcpy(str_copy, str);
    
    char* cursor = str_copy;
    char* line_end;
    int row = 0;
    
    // Outer loop: Iterate over lines manually using strchr
    // This avoids using strtok's static state for the outer loop
    while (row < size && ((line_end = strchr(cursor, '\n')) != NULL || *cursor != '\0')) {
        // If we found a newline, terminate the string there temporarily
        if (line_end) {
            *line_end = '\0';
        }
        
        // Skip separator lines (starting with -)
        if (cursor[0] == '-') {
            if (line_end) cursor = line_end + 1;
            else break;
            continue;
        }
        // Inner loop: Use strtok safely to parse numbers within the line
        // We need a copy because strtok modifies the string
        char* line_copy = (char*)malloc(strlen(cursor) + 1);
        strcpy(line_copy, cursor);
        
        char* token = strtok(line_copy, " |\t");
        int col = 0;
        
        while (token != NULL && col < size) {
            if (strlen(token) == 1) {
                int num = char_to_num(token[0]);
                if (num >= 0 && num <= size) {
                    sudoku->grid[row][col] = num;
                    col++;
                }
            } else {
                char* endptr;
                int num = (int)strtol(token, &endptr, 10);
                if (endptr != token && *endptr == '\0' && num >= 0 && num <= size) {
                    sudoku->grid[row][col] = num;
                    col++;
                }
            }
            
            token = strtok(NULL, " |\t");
        }
        
        free(line_copy);
        
        if (col > 0) {
            row++;
        }
        
        // Move cursor to the character after the newline
        if (line_end) {
            cursor = line_end + 1;
        } else {
            break; // End of string
        }
    }
    
    free(str_copy);
    return sudoku;
}
