
#include "../include/backtracking.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

// --- Protótipos das Funções ---

// Funções de Validação ("Trabalhadoras")
bool is_in_row(Sudoku* sudoku, int r, int num);
bool is_in_col(Sudoku* sudoku, int c, int num);
bool is_in_box(Sudoku* sudoku, int r, int c, int num);
bool is_safe(Sudoku* sudoku, int r, int c, int num);

// Funções de Estratégia ("Ajudantes")
int find_all_empty_cells(Sudoku* sudoku, Coordenada lista_vazias[]);
int find_next_valid_number(Sudoku* sudoku, int r, int c, int num_inicio);

/**
 * Funcao "Chefe" / Orquestradora.
 * Gerencia o estado (k) e coordena o avanço/recuo.
 */
SolveResult solve_sudoku_iterativo(Sudoku* sudoku) {
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


/**
 * RESPONSABILIDADE: Preparar a lista de "trabalhos".
 * Varre o tabuleiro e preenche o array 'lista_vazias'.
 * Retorna: o número total de células vazias.
 */
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

/**
 * RESPONSABILIDADE: Encontrar o próximo número válido (de num_inicio a 9).
 * Retorna: o número (1-9) se encontrar, ou 10 se falhar (N+1).
 */
int find_next_valid_number(Sudoku* sudoku, int r, int c, int num_inicio) {
    for (int num = num_inicio; num <= sudoku->size; num++) {
        if (is_safe(sudoku, r, c, num)) {
            return num; // Encontrou um número válido
        }
    }
    // Tentou de 'num_inicio' até 9 e nenhum funcionou
    return sudoku->size + 1; // Sinal de falha
}


/**
 * RESPONSABILIDADE: Checar se 'num' é seguro para colocar em board[r][c].
 * Delega para as funções especialistas.
 */
bool is_safe(Sudoku* sudoku, int r, int c, int num) {
    return !is_in_row(sudoku, r, num) &&
           !is_in_col(sudoku, c, num) &&
           !is_in_box(sudoku, r, c, num);
}

/**
 * RESPONSABILIDADE: Verifica se 'num' já existe na linha 'r'.
 */
bool is_in_row(Sudoku* sudoku, int r, int num) {
    for (int c = 0; c < sudoku->size; c++) {
        if (sudoku->grid[r][c] == num) {
            return true;
        }
    }
    return false;
}

/**
 * RESPONSABILIDADE: Verifica se 'num' já existe na coluna 'c'.
 */
bool is_in_col(Sudoku* sudoku, int c, int num) {
    for (int r = 0; r < sudoku->size; r++) {
        if (sudoku->grid[r][c] == num) {
            return true;
        }
    }
    return false;
}

/**
 * RESPONSABILIDADE: Verifica se 'num' já existe no bloco 3x3.
 */
bool is_in_box(Sudoku* sudoku, int r, int c, int num) {
    // Encontra o canto superior esquerdo do bloco 3x3
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
