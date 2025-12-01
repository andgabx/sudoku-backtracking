#include "../include/sudoku.h"
#include "../include/backtracking.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {

    if (argc != 3 && argc != 4) {
        printf("Uso: %s <size> <case> [puzzle_file]\n", argv[0]);
        printf("  size: small, medium, large\n");
        printf("  case: best, worst\n");
        printf("  puzzle_file: (opcional) arquivo com puzzles pré-gerados\n");
        printf("               Se não fornecido, usa puzzle_seeds/{size}_{case}.txt\n");
        return 1;
    }
    
    char* size_str = argv[1];
    char* case_str = argv[2];
    
    int size;
    int empty_cells;
    
    if (strcmp(size_str, "small") == 0) {
        size = 4;
        empty_cells = (strcmp(case_str, "best") == 0) ? 5 : 8;  // best=30%, worst=50%
    } else if (strcmp(size_str, "medium") == 0) {
        size = 9;
        empty_cells = (strcmp(case_str, "best") == 0) ? 24 : 40; // best=30%, worst=50%
    } else if (strcmp(size_str, "large") == 0) {
        size = 16;
        empty_cells = (strcmp(case_str, "best") == 0) ? 77 : 128; // best=30%, worst=50%
    } else {
        printf("Tamanho inválido. Use: small, medium ou large\n");
        return 1;
    }
    
    char log_filename[256];
    snprintf(log_filename, sizeof(log_filename), "../../logs/c_%s_%s.log", size_str, case_str);
    
    FILE* log_file = fopen(log_filename, "w");
    if (!log_file) {
        printf("Erro ao criar arquivo de log: %s\n", log_filename);
        return 1;
    }
    
    fprintf(log_file, "=== Análise de Complexidade - Backtracking Iterativo para Sudoku ===\n");
    fprintf(log_file, "Linguagem: C\n");
    fprintf(log_file, "Tamanho: %dx%d\n", size, size);
    fprintf(log_file, "Caso: %s\n", case_str);
    fprintf(log_file, "Células vazias alvo: %d\n", empty_cells);
    fprintf(log_file, "Número de execuções: 30\n\n");
    
    double total_time = 0.0;
    long long total_iterations = 0;
    int successful_solves = 0;
    
    printf("Executando 30 testes para %s %s em C...\n", size_str, case_str);
    
    // Determinar arquivo de puzzles
    char puzzle_filename[256];
    if (argc == 4) {
        strncpy(puzzle_filename, argv[3], sizeof(puzzle_filename) - 1);
        puzzle_filename[sizeof(puzzle_filename) - 1] = '\0';
    } else {
        snprintf(puzzle_filename, sizeof(puzzle_filename), "../../puzzle_seeds/%s_%s.txt", size_str, case_str);
    }
    
    FILE* puzzle_file = fopen(puzzle_filename, "r");
    if (!puzzle_file) {
        printf("Erro: Não foi possível abrir arquivo de puzzles: %s\n", puzzle_filename);
        printf("Execute primeiro: make build-generator && ./c/bin/puzzle_generator\n");
        return 1;
    }
    printf("  Carregando puzzles de: %s\n", puzzle_filename);
    
    for (int run = 1; run <= 30; run++) {
        
        Sudoku* sudoku = load_puzzle_from_file(puzzle_file, size);
        if (!sudoku) {
            printf("Erro: Não foi possível carregar puzzle %d do arquivo\n", run);
            fclose(puzzle_file);
            return 1;
        }
        
        int actual_empty = count_empty_cells(sudoku);
        
        printf("\n=== Execução %d/30 ===\n", run);
        printf("  Resolvendo puzzle... (pode demorar para puzzles grandes)\n");
        fflush(stdout);  // Garante que a mensagem aparece imediatamente
        
        SolveResult result = solve_sudoku_iterative(sudoku);

        
        fprintf(log_file, "Execução %d:\n", run);
        fprintf(log_file, "  Células vazias: %d\n", actual_empty);
        fprintf(log_file, "  Tempo: %.6f segundos\n", result.time_seconds);
        fprintf(log_file, "  Iterações: %lld\n", result.iterations);
        fprintf(log_file, "  Resolvido: %s\n\n", result.solved ? "Sim" : "Não");
        
        if (result.solved) {
            total_time += result.time_seconds;
            total_iterations += result.iterations;
            successful_solves++;
        }
        
        sudoku_destroy(sudoku);
        
        printf("  Execução %d/%d concluída (%.6fs, %lld iterações)\n", 
               run, 30, result.time_seconds, result.iterations);
        fflush(stdout);  // Garante que a mensagem aparece imediatamente
    }
    
    fclose(puzzle_file);
    
    fprintf(log_file, "=== ESTATÍSTICAS FINAIS ===\n");
    fprintf(log_file, "Resoluções bem-sucedidas: %d/30\n", successful_solves);
    
    if (successful_solves > 0) {
        double avg_time = total_time / successful_solves;
        double avg_iterations = (double)total_iterations / successful_solves;
        
        fprintf(log_file, "Tempo médio: %.6f segundos\n", avg_time);
        fprintf(log_file, "Tempo total: %.6f segundos\n", total_time);
        fprintf(log_file, "Iterações médias: %.2f\n", avg_iterations);
        fprintf(log_file, "Iterações totais: %lld\n", total_iterations);
        
        printf("\n✓ Análise concluída!\n");
        printf("  Tempo médio: %.6f segundos\n", avg_time);
        printf("  Iterações médias: %.2f\n", avg_iterations);
    }
    
    fclose(log_file);
    printf("  Log salvo em: %s\n", log_filename);
    
    return 0;
}
