#ifndef SUDOKU_H
#define SUDOKU_H

#include <stdbool.h>
#include <stdio.h>

typedef struct {
    int** grid;
    int size;      
    int box_size;  
} Sudoku;

Sudoku* sudoku_create(int size);
void sudoku_destroy(Sudoku* sudoku);
bool is_valid(Sudoku* sudoku, int row, int col, int num);
void sudoku_print(Sudoku* sudoku);
int count_empty_cells(Sudoku* sudoku);
Sudoku* sudoku_parse_from_string(const char* str, int size);
Sudoku* load_puzzle_from_file(FILE* file, int size);

#endif 
