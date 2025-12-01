#include "../include/generator.h"
#include "../include/sudoku.h"
#include <stdlib.h>
#include <string.h>

// Estado global do LCG
static unsigned int lcg_state = 0;

void lcg_seed(unsigned int seed) {
    lcg_state = seed & 0x7fffffff;
}

unsigned int lcg_next(void) {
    // LCG: (a * state + c) mod m
    // a = 1103515245, c = 12345, m = 2^31
    lcg_state = (1103515245U * lcg_state + 12345U) & 0x7fffffff;
    return lcg_state;
}

// Shuffle usando Fisher-Yates com LCG
static void shuffle(int* array, int n) {
    for (int i = n - 1; i > 0; i--) {
        int j = lcg_next() % (i + 1);
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

// Contador global para limitar tentativas (evita travamentos)
static int fill_attempts = 0;
static const int MAX_FILL_ATTEMPTS = 1000000;  // Limite de tentativas

bool fill_sudoku(Sudoku* sudoku, int row, int col) {
    // Limite de segurança para evitar travamentos
    if (fill_attempts++ > MAX_FILL_ATTEMPTS) {
        return false;
    }
    
    if (row == sudoku->size) {
        return true;
    }
    
    int next_row = (col == sudoku->size - 1) ? row + 1 : row;
    int next_col = (col == sudoku->size - 1) ? 0 : col + 1;
    
    // Cria array de números e embaralha
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

Sudoku* generate_sudoku(int size, int empty_cells, unsigned int seed) {
    Sudoku* sudoku = sudoku_create(size);
    
    // Tenta preencher o Sudoku com uma solução válida
    // Se falhar, tenta com seed diferente (incrementa)
    int attempts = 0;
    unsigned int current_seed = seed;
    while (attempts < 20) {  // Aumentado para 20 tentativas
        fill_attempts = 0;  // Reset contador
        lcg_seed(current_seed);
        // Limpa o Sudoku
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                sudoku->grid[i][j] = 0;
            }
        }
        
        if (fill_sudoku(sudoku, 0, 0)) {
            break;  // Sucesso!
        }
        
        // Se falhou, tenta com seed diferente (usa multiplicação para variar mais)
        current_seed = seed + (attempts + 1) * 7919;  // 7919 é um primo para melhor distribuição
        attempts++;
    }
    
    if (attempts >= 20) {
        // Se ainda falhou após 20 tentativas, retorna NULL
        sudoku_destroy(sudoku);
        return NULL;
    }
    
    // Remove células aleatoriamente usando Fisher-Yates
    int total_cells = size * size;
    int* positions = (int*)malloc(total_cells * sizeof(int));
    for (int i = 0; i < total_cells; i++) {
        positions[i] = i;
    }
    shuffle(positions, total_cells);
    
    int cells_to_remove = (empty_cells < total_cells) ? empty_cells : total_cells;
    for (int i = 0; i < cells_to_remove; i++) {
        int pos = positions[i];
        int row = pos / size;
        int col = pos % size;
        sudoku->grid[row][col] = 0;
    }
    
    free(positions);
    return sudoku;
}

char num_to_char(int num) {
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

void sudoku_to_string(Sudoku* sudoku, char* buffer, int buffer_size) {
    buffer[0] = '\0';
    int pos = 0;
    
    for (int i = 0; i < sudoku->size; i++) {
        if (i % sudoku->box_size == 0 && i != 0) {
            // Linha separadora
            for (int k = 0; k < sudoku->size * 2 + sudoku->box_size - 1; k++) {
                if (pos < buffer_size - 1) {
                    buffer[pos++] = '-';
                }
            }
            if (pos < buffer_size - 1) {
                buffer[pos++] = '\n';
            }
        }
        
        for (int j = 0; j < sudoku->size; j++) {
            if (j % sudoku->box_size == 0 && j != 0) {
                if (pos < buffer_size - 2) {
                    buffer[pos++] = ' ';
                    buffer[pos++] = '|';
                    buffer[pos++] = ' ';
                }
            }
            
            if (j > 0 && !(j % sudoku->box_size == 0)) {
                if (pos < buffer_size - 1) {
                    buffer[pos++] = ' ';
                }
            }
            
            if (pos < buffer_size - 1) {
                buffer[pos++] = num_to_char(sudoku->grid[i][j]);
            }
        }
        
        if (pos < buffer_size - 1) {
            buffer[pos++] = '\n';
        }
    }
    
    buffer[pos] = '\0';
}

