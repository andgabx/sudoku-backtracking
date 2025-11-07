
"""
Programa principal para análise de complexidade do backtracking em Sudoku
"""
import sys
import os
from sudoku import Sudoku
from backtracking import solve_sudoku_iterativo
from generator import generate_sudoku

def main():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <size> <case>")
        print("  size: small, medium, large")
        print("  case: best, worst")
        sys.exit(1)
    
    size_str = sys.argv[1]
    case_str = sys.argv[2]
    
    # Define tamanho do Sudoku e células vazias
    size_map = {
        'small': (3, 2, 5),   # (size, best_empty, worst_empty)
        'medium': (6, 9, 22),
        'large': (9, 23, 55)
    }
    
    if size_str not in size_map:
        print("Tamanho inválido. Use: small, medium ou large")
        sys.exit(1)
    
    size, best_empty, worst_empty = size_map[size_str]
    empty_cells = best_empty if case_str == 'best' else worst_empty
    
    # Nome do arquivo de log (caminho relativo ao diretório raiz do projeto)
    log_filename = f"../../logs/python_{size_str}_{case_str}.log"
    
    # Cria diretório logs se não existir
    os.makedirs('../../logs', exist_ok=True)
    
    with open(log_filename, 'w') as log_file:
        log_file.write("=== Análise de Complexidade - Backtracking Iterativo para Sudoku ===\n")
        log_file.write("Linguagem: Python\n")
        log_file.write(f"Tamanho: {size}x{size}\n")
        log_file.write(f"Caso: {case_str}\n")
        log_file.write(f"Células vazias alvo: {empty_cells}\n")
        log_file.write("Número de execuções: 30\n\n")
        
        total_time = 0.0
        total_iterations = 0
        successful_solves = 0
        
        print(f"Executando 30 testes para {size_str} {case_str} em Python...")
        
        for run in range(1, 31):
            # Gera novo puzzle
            sudoku = generate_sudoku(size, empty_cells)
            actual_empty = sudoku.count_empty_cells()
            
            # Resolve o puzzle
            result = solve_sudoku_iterativo(sudoku)
            
            log_file.write(f"Execução {run}:\n")
            log_file.write(f"  Células vazias: {actual_empty}\n")
            log_file.write(f"  Tempo: {result.time_seconds:.6f} segundos\n")
            log_file.write(f"  Iterações: {result.iterations}\n")
            log_file.write(f"  Resolvido: {'Sim' if result.solved else 'Não'}\n\n")
            
            if result.solved:
                total_time += result.time_seconds
                total_iterations += result.iterations
                successful_solves += 1
            
            print(f"  Execução {run}/30 concluída "
                  f"({result.time_seconds:.6f}s, {result.iterations} iterações)")
        
        # Estatísticas finais
        log_file.write("=== ESTATÍSTICAS FINAIS ===\n")
        log_file.write(f"Resoluções bem-sucedidas: {successful_solves}/30\n")
        
        if successful_solves > 0:
            avg_time = total_time / successful_solves
            avg_iterations = total_iterations / successful_solves
            
            log_file.write(f"Tempo médio: {avg_time:.6f} segundos\n")
            log_file.write(f"Tempo total: {total_time:.6f} segundos\n")
            log_file.write(f"Iterações médias: {avg_iterations:.2f}\n")
            log_file.write(f"Iterações totais: {total_iterations}\n")
            
            print(f"\n✓ Análise concluída!")
            print(f"  Tempo médio: {avg_time:.6f} segundos")
            print(f"  Iterações médias: {avg_iterations:.2f}")
    
    print(f"  Log salvo em: {log_filename}")

if __name__ == "__main__":
    main()
