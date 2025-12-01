#include "../include/generator.h"
#include "../include/sudoku.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

// Hash simples para gerar seed baseada em string
unsigned int hash_string(const char* str) {
    unsigned int hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

void generate_puzzles_for_config(const char* size_str, const char* case_str, int num_puzzles) {
    int size, best_empty, worst_empty;
    
    if (strcmp(size_str, "small") == 0) {
        size = 4;
        best_empty = 5;   // 30% - mais fácil (menos células vazias)
        worst_empty = 8;  // 50% - mais difícil (mais células vazias)
    } else if (strcmp(size_str, "medium") == 0) {
        size = 9;
        best_empty = 24;  // 30% - mais fácil (menos células vazias)
        worst_empty = 40; // 50% - mais difícil (mais células vazias)
    } else if (strcmp(size_str, "large") == 0) {
        size = 16;
        best_empty = 77;   // 30% - mais fácil (menos células vazias)
        worst_empty = 128; // 50% - mais difícil (mais células vazias)
    } else {
        fprintf(stderr, "Tamanho inválido: %s\n", size_str);
        exit(1);
    }
    
    int empty_cells = (strcmp(case_str, "best") == 0) ? best_empty : worst_empty;
    
    // Cria diretório puzzle_seeds se não existir (na raiz do projeto)
    mkdir("../../puzzle_seeds", 0755);
    
    char filename[256];
    snprintf(filename, sizeof(filename), "../../puzzle_seeds/%s_%s.txt", size_str, case_str);
    
    FILE* file = fopen(filename, "w");
    if (!file) {
        fprintf(stderr, "Erro ao criar arquivo: %s\n", filename);
        exit(1);
    }
    
    printf("Gerando %d puzzles para %s %s...\n", num_puzzles, size_str, case_str);
    
    char buffer[8192];
    for (int i = 1; i <= num_puzzles; i++) {
        // Gera seed baseada no índice
        unsigned int seed = i * 1000 + hash_string(size_str) + hash_string(case_str);
        
        Sudoku* sudoku = generate_sudoku(size, empty_cells, seed);
        
        if (!sudoku) {
            fprintf(stderr, "ERRO: Não foi possível gerar puzzle %d/%d\n", i, num_puzzles);
            continue;
        }
        
        // Escreve cabeçalho do puzzle
        fprintf(file, "=== Puzzle %d/%d ===\n", i, num_puzzles);
        
        // Converte Sudoku para string e escreve
        sudoku_to_string(sudoku, buffer, sizeof(buffer));
        fprintf(file, "%s", buffer);
        fprintf(file, "\n\n");
        
        sudoku_destroy(sudoku);
        
        if (i % 10 == 0) {
            printf("  Gerados %d/%d puzzles...\n", i, num_puzzles);
        }
    }
    
    fclose(file);
    printf("✓ %d puzzles salvos em: %s\n", num_puzzles, filename);
}

int main(int argc, char* argv[]) {
    if (argc == 1) {
        // Gera todos os puzzles
        printf("============================================================\n");
        printf("Gerando arquivos de puzzles pré-gerados\n");
        printf("============================================================\n");
        printf("\n");
        
        const char* configs[][2] = {
            {"small", "best"},
            {"small", "worst"},
            {"medium", "best"},
            {"medium", "worst"},
            {"large", "best"},
            {"large", "worst"}
        };
        
        for (int i = 0; i < 6; i++) {
            generate_puzzles_for_config(configs[i][0], configs[i][1], 30);
            printf("\n");
        }
        
        printf("============================================================\n");
        printf("✓ Todos os puzzles foram gerados com sucesso!\n");
        printf("============================================================\n");
    } else if (argc == 3) {
        // Gera para uma configuração específica
        generate_puzzles_for_config(argv[1], argv[2], 30);
    } else {
        fprintf(stderr, "Uso: %s [size case]\n", argv[0]);
        fprintf(stderr, "  size: small, medium, large\n");
        fprintf(stderr, "  case: best, worst\n");
        fprintf(stderr, "  Se nenhum argumento for fornecido, gera todos os puzzles\n");
        exit(1);
    }
    
    return 0;
}

