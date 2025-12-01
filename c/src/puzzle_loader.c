#include "../include/sudoku.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Lê um puzzle de um arquivo de texto
// Retorna o Sudoku ou NULL se houver erro
Sudoku* load_puzzle_from_file(FILE* file, int size) {
    char buffer[4096] = {0};
    char puzzle_str[2048] = {0};
    int puzzle_started = 0;
    int puzzle_line_count = 0;
    
    // Procura pelo início de um puzzle (linha com "=== Puzzle")
    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        if (strstr(buffer, "=== Puzzle") != NULL) {
            puzzle_started = 1;
            puzzle_line_count = 0;
            puzzle_str[0] = '\0';
            continue;
        }
        
        if (puzzle_started) {
            // Se encontrou linha vazia após puzzle, terminou
            if (strlen(buffer) <= 1) {
                break;
            }
            
            // Adiciona linha ao puzzle_str
            strcat(puzzle_str, buffer);
            puzzle_line_count++;
            
            // Para Sudoku 4x4: ~6 linhas, 9x9: ~13 linhas, 16x16: ~21 linhas
            if (puzzle_line_count > size + (size / 3) + 2) {
                break;
            }
        }
    }
    
    if (puzzle_str[0] == '\0') {
        return NULL;
    }
    
    return sudoku_parse_from_string(puzzle_str, size);
}

