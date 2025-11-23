#!/usr/bin/env python3
"""
Script para gerar arquivos de texto com Sudokus pré-gerados.
Gera 30 Sudokus para cada combinação (size × case) e salva em formato texto.
"""

import sys
from pathlib import Path

# Adiciona o diretório python/src ao path
sys.path.insert(0, str(Path(__file__).parent / 'python' / 'src'))

from sudoku import Sudoku
from generator import generate_sudoku

def sudoku_to_string(sudoku: Sudoku) -> str:
    """Converte um Sudoku para string no formato de impressão."""
    lines = []
    for i in range(sudoku.size):
        if i % sudoku.box_size == 0 and i != 0:
            lines.append("-" * (sudoku.size * 2 + sudoku.box_size - 1))
        
        row_parts = []
        for j in range(sudoku.size):
            if j % sudoku.box_size == 0 and j != 0:
                row_parts.append("|")
            row_parts.append(str(sudoku.grid[i][j]))
        
        lines.append(" ".join(row_parts))
    
    return "\n".join(lines)

def generate_puzzles_for_config(size_str: str, case_str: str, num_puzzles: int = 30):
    """Gera puzzles para uma configuração específica."""
    size_map = {
        'small': (3, 2, 5),
        'medium': (6, 9, 22),
        'large': (9, 23, 55)
    }
    
    if size_str not in size_map:
        raise ValueError(f"Tamanho inválido: {size_str}")
    
    size, best_empty, worst_empty = size_map[size_str]
    empty_cells = best_empty if case_str == 'best' else worst_empty
    
    puzzles_dir = Path(__file__).parent / 'puzzle_seeds'
    puzzles_dir.mkdir(exist_ok=True)
    
    output_file = puzzles_dir / f"{size_str}_{case_str}.txt"
    
    print(f"Gerando {num_puzzles} puzzles para {size_str} {case_str}...")
    
    with open(output_file, 'w') as f:
        for i in range(1, num_puzzles + 1):
            # Gera um Sudoku com seed baseada no índice para garantir reprodutibilidade
            seed = i * 1000 + hash(f"{size_str}_{case_str}")
            sudoku = generate_sudoku(size, empty_cells, seed=seed)
            
            # Salva o puzzle
            puzzle_str = sudoku_to_string(sudoku)
            f.write(f"=== Puzzle {i}/{num_puzzles} ===\n")
            f.write(puzzle_str)
            f.write("\n\n")
            
            if i % 10 == 0:
                print(f"  Gerados {i}/{num_puzzles} puzzles...")
    
    print(f"✓ {num_puzzles} puzzles salvos em: {output_file}")
    return output_file

def main():
    """Gera todos os arquivos de puzzles."""
    configs = [
        ('small', 'best'),
        ('small', 'worst'),
        ('medium', 'best'),
        ('medium', 'worst'),
        ('large', 'best'),
        ('large', 'worst'),
    ]
    
    print("="*60)
    print("Gerando arquivos de puzzles pré-gerados")
    print("="*60)
    print()
    
    for size_str, case_str in configs:
        try:
            generate_puzzles_for_config(size_str, case_str, 30)
            print()
        except Exception as e:
            print(f"Erro ao gerar {size_str} {case_str}: {e}")
            sys.exit(1)
    
    print("="*60)
    print("✓ Todos os puzzles foram gerados com sucesso!")
    print("="*60)

if __name__ == "__main__":
    main()

