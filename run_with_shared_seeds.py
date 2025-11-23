#!/usr/bin/env python3
"""
Script para executar testes com puzzles compartilhados entre C e Python.
Garante que cada execução (1-30) use o mesmo puzzle em ambas as linguagens.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test_with_puzzles(size, case, lang, puzzle_file=None):
    """Executa um teste com puzzles pré-gerados."""
    project_root = Path(__file__).parent
    
    if lang == 'c':
        bin_dir = project_root / 'c' / 'bin'
        if puzzle_file:
            # Converter caminho relativo para absoluto
            abs_puzzle_file = os.path.abspath(puzzle_file)
            cmd = [str(bin_dir / 'sudoku_solver'), size, case, abs_puzzle_file]
        else:
            cmd = [str(bin_dir / 'sudoku_solver'), size, case]
        cwd = bin_dir
    else:  # python
        src_dir = project_root / 'python' / 'src'
        if puzzle_file:
            # Converter caminho relativo para absoluto
            abs_puzzle_file = os.path.abspath(puzzle_file)
            cmd = ['python3', 'main.py', size, case, abs_puzzle_file]
        else:
            cmd = ['python3', 'main.py', size, case]
        cwd = src_dir
    
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 run_with_shared_seeds.py <size> <case>")
        print("  size: small, medium, large")
        print("  case: best, worst")
        sys.exit(1)
    
    size = sys.argv[1]
    case = sys.argv[2]
    
    project_root = Path(__file__).parent
    puzzle_file = project_root / 'puzzle_seeds' / f"{size}_{case}.txt"
    
    if not puzzle_file.exists():
        print(f"Erro: Arquivo de puzzles não encontrado: {puzzle_file}")
        print("Execute primeiro: python3 generate_sudoku_puzzles.py")
        sys.exit(1)
    
    print(f"Usando puzzles pré-gerados de: {puzzle_file}")
    print()
    
    # Executar C primeiro
    print("="*60)
    print(f"Executando testes em C para {size} {case}...")
    print("="*60)
    success_c, stdout_c, stderr_c = run_test_with_puzzles(size, case, 'c', puzzle_file=str(puzzle_file))
    if not success_c:
        print(f"Erro ao executar C: {stderr_c}")
        sys.exit(1)
    print(stdout_c)
    
    print()
    
    # Executar Python depois
    print("="*60)
    print(f"Executando testes em Python para {size} {case}...")
    print("="*60)
    success_py, stdout_py, stderr_py = run_test_with_puzzles(size, case, 'python', puzzle_file=str(puzzle_file))
    if not success_py:
        print(f"Erro ao executar Python: {stderr_py}")
        sys.exit(1)
    print(stdout_py)
    
    print()
    print("="*60)
    print("✓ Testes concluídos com puzzles compartilhados!")
    print(f"  Puzzles carregados de: {puzzle_file}")
    print("="*60)

if __name__ == "__main__":
    main()

