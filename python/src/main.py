import sys
import os
from sudoku import Sudoku
from backtracking import solve_sudoku_iterativo

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print(f"Uso: {sys.argv[0]} <size> <case> [puzzle_file]")
        print("  size: small, medium, large")
        print("  case: best, worst")
        print("  puzzle_file: (opcional) arquivo com puzzles pré-gerados")
        sys.exit(1)
    
    size_str = sys.argv[1]
    case_str = sys.argv[2]
    
    # Define tamanho do Sudoku e células vazias

    size_map = {
        'small': (4, 8, 5),        # 4x4: best=8 (50%), worst=5 (31%)
        'medium': (9, 40, 24),     # 9x9: best=40 (49%), worst=24 (30%)
        'large': (16, 128, 77)     # 16x16: best=128 (50%), worst=77 (30%)
    }
    
    if size_str not in size_map:
        print("Tamanho inválido. Use: small, medium ou large")
        sys.exit(1)
    
    size, best_empty, worst_empty = size_map[size_str]
    empty_cells = best_empty if case_str == 'best' else worst_empty
    
    log_filename = f"../../logs/python_{size_str}_{case_str}.log"
    
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
        
        # Determinar arquivo de puzzles
        if len(sys.argv) == 4:
            puzzle_file_path = sys.argv[3]
        else:
            puzzle_file_path = f"../../puzzle_seeds/{size_str}_{case_str}.txt"
        
        try:
            with open(puzzle_file_path, 'r') as f:
                puzzle_content = f.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo de puzzles não encontrado: {puzzle_file_path}")
            print("Execute primeiro: make build-generator && ./c/bin/puzzle_generator")
            sys.exit(1)
        
        print(f"  Carregando puzzles de: {puzzle_file_path}")
        
        # Parse puzzles do arquivo
        puzzles = []
        puzzle_sections = puzzle_content.split("=== Puzzle")
        for section in puzzle_sections[1:]:  # Pula o primeiro (vazio)
            # Extrai o número do puzzle e o conteúdo
            lines = section.strip().split('\n')
            if len(lines) > 1:
                puzzle_str = '\n'.join(lines[1:])  # Remove a linha "=== Puzzle X/30 ==="
                sudoku = Sudoku.parse_from_string(puzzle_str, size)
                puzzles.append(sudoku)
        
        if len(puzzles) < 30:
            print(f"  Aviso: Apenas {len(puzzles)} puzzles encontrados no arquivo")
        
        for run in range(1, min(31, len(puzzles) + 1)):
            sudoku = puzzles[run - 1]
            actual_empty = sudoku.count_empty_cells()
            
            print(f"\n=== Execução {run}/30 ===")
            print("  Resolvendo puzzle... (pode demorar para puzzles grandes)")
            
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
