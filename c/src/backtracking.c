#include "../include/backtracking.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

SolveResult solve_sudoku_iterative(Sudoku* sudoku) {
    SolveResult result;
    result.iterations = 0;
    result.solved = false;
    
    clock_t start = clock();

    // 1. Encontrar todas as células para preencher
    Coordenada* lista_vazias = (Coordenada*)malloc(sizeof(Coordenada) * sudoku->size * sudoku->size);
    int total_vazias = find_all_empty_cells(sudoku, lista_vazias);

    // Se não há células vazias, já está resolvido
    if (total_vazias == 0) {
        result.solved = true;
        clock_t end = clock();
        result.time_seconds = (double)(end - start) / CLOCKS_PER_SEC;
        return result;
    }

    int k = 0; // Índice da célula vazia atual (nosso "estado")

    // Loop principal do backtracking
    // k == total_vazias -> Solução encontrada
    // k == -1 -> Beco sem saída total
    while (k >= 0 && k < total_vazias) {
        result.iterations++;
      
        Coordenada cell = lista_vazias[k];
        int r = cell.row;
        int c = cell.col;

        // Pega o valor que estava lá (se for 0, começa do 1; se 5, começa do 6)
        int num_inicio = sudoku->grid[r][c] + 1;

        // 2. Encontrar o próximo número válido para esta célula
        int num_valido = find_next_valid_number(sudoku, r, c, num_inicio);

        if (num_valido <= sudoku->size) {
            // SUCESSO: Encontramos um número válido
            sudoku->grid[r][c] = num_valido;
            k++; // AVANÇA para a próxima célula vazia
        } else {
            // FALHA: Nenhum número de 'num_inicio' até 9 funcionou
            sudoku->grid[r][c] = 0;   // LIMPA a célula (o ato do Backtrack)
            k--;               // RECUA para a célula anterior
        }
    }

    clock_t end = clock();
    result.time_seconds = (double)(end - start) / CLOCKS_PER_SEC;
    result.solved = k == total_vazias;

    free(lista_vazias);
    
    return result;
}


int find_all_empty_cells(Sudoku* sudoku, Coordenada lista_vazias[]) {
    int count = 0;
    for (int r = 0; r < sudoku->size; r++) {
        for (int c = 0; c < sudoku->size; c++) {
            if (sudoku->grid[r][c] == 0) {
                lista_vazias[count].row = r;
                lista_vazias[count].col = c;
                count++;
            }
        }
    }
    return count;
}

int find_next_valid_number(Sudoku* sudoku, int r, int c, int num_inicio) {
    for (int num = num_inicio; num <= sudoku->size; num++) {
        if (is_safe(sudoku, r, c, num)) {
            return num; // Encontrou um número válido
        }
    }
    return sudoku->size + 1; // Sinal de falha
}

bool is_safe(Sudoku* sudoku, int r, int c, int num) {
    return !is_in_row(sudoku, r, num) &&
           !is_in_col(sudoku, c, num) &&
           !is_in_box(sudoku, r, c, num);
}

bool is_in_row(Sudoku* sudoku, int r, int num) {
    for (int c = 0; c < sudoku->size; c++) {
        if (sudoku->grid[r][c] == num) {
            return true;
        }
    }
    return false;
}

bool is_in_col(Sudoku* sudoku, int c, int num) {
    for (int r = 0; r < sudoku->size; r++) {
        if (sudoku->grid[r][c] == num) {
            return true;
        }
    }
    return false;
}

bool is_in_box(Sudoku* sudoku, int r, int c, int num) {

    int box_start_row = r - r % sudoku->box_size;
    int box_start_col = c - c % sudoku->box_size;

    for (int i = 0; i < sudoku->box_size; i++) {
        for (int j = 0; j < sudoku->box_size; j++) {
            if (sudoku->grid[box_start_row + i][box_start_col + j] == num) {
                return true;
            }
        }
    }
    return false;
}
