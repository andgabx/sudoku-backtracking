
"""
Módulo de backtracking iterativo para resolver Sudoku
"""
import time
from typing import NamedTuple, List, Tuple
from sudoku import Sudoku

class Coordenada(NamedTuple):
    """Estrutura para armazenar as coordenadas de uma célula"""
    row: int
    col: int

class SolveResult(NamedTuple):
    """Resultado da resolução do Sudoku"""
    time_seconds: float
    iterations: int
    solved: bool

def solve_sudoku_iterativo(sudoku: Sudoku) -> SolveResult:
    """
    Resolve o Sudoku usando backtracking iterativo com lista de células vazias.
    """
    start_time = time.time()
    iterations = 0

    # 1. Encontrar todas as células para preencher
    lista_vazias = _find_all_empty_cells(sudoku)
    total_vazias = len(lista_vazias)

    if total_vazias == 0:
        end_time = time.time()
        return SolveResult(time_seconds=end_time - start_time, iterations=0, solved=True)

    k = 0  # Índice da célula vazia atual

    while -1 < k < total_vazias:
        iterations += 1
        
        # Print de progresso a cada 10 milhões de iterações (para puzzles grandes)
        if iterations % 10000000 == 0:
            print(f"  ... {iterations} iterações e contando...")
        
        cell = lista_vazias[k]
        r, c = cell.row, cell.col

        num_inicio = sudoku.grid[r][c] + 1
        
        num_valido = _find_next_valid_number(sudoku, r, c, num_inicio)

        if num_valido <= sudoku.size:
            sudoku.grid[r][c] = num_valido
            k += 1
        else:
            sudoku.grid[r][c] = 0
            k -= 1
            
    end_time = time.time()
    solved = k == total_vazias
    return SolveResult(time_seconds=end_time - start_time, iterations=iterations, solved=solved)

def _find_all_empty_cells(sudoku: Sudoku) -> List[Coordenada]:
    """Encontra todas as células vazias e retorna uma lista de coordenadas."""
    empty_cells = []
    for r in range(sudoku.size):
        for c in range(sudoku.size):
            if sudoku.grid[r][c] == 0:
                empty_cells.append(Coordenada(r, c))
    return empty_cells

def _find_next_valid_number(sudoku: Sudoku, r: int, c: int, num_inicio: int) -> int:
    """Encontra o próximo número válido para a célula [r][c]."""
    for num in range(num_inicio, sudoku.size + 1):
        if _is_safe(sudoku, r, c, num):
            return num
    return sudoku.size + 1

def _is_safe(sudoku: Sudoku, r: int, c: int, num: int) -> bool:
    """Verifica se é seguro colocar 'num' na célula [r][c]."""
    return not _is_in_row(sudoku, r, num) and \
           not _is_in_col(sudoku, c, num) and \
           not _is_in_box(sudoku, r, c, num)

def _is_in_row(sudoku: Sudoku, r: int, num: int) -> bool:
    """Verifica se 'num' já existe na linha 'r'."""
    for c in range(sudoku.size):
        if sudoku.grid[r][c] == num:
            return True
    return False

def _is_in_col(sudoku: Sudoku, c: int, num: int) -> bool:
    """Verifica se 'num' já existe na coluna 'c'."""
    for r in range(sudoku.size):
        if sudoku.grid[r][c] == num:
            return True
    return False

def _is_in_box(sudoku: Sudoku, r: int, c: int, num: int) -> bool:
    """Verifica se 'num' já existe no bloco (box_size x box_size)."""
    box_start_row = r - r % sudoku.box_size
    box_start_col = c - c % sudoku.box_size
    for i in range(sudoku.box_size):
        for j in range(sudoku.box_size):
            if sudoku.grid[box_start_row + i][box_start_col + j] == num:
                return True
    return False
