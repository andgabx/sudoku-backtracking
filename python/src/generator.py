import random
from sudoku import Sudoku

# gera sudokus validos

def fill_sudoku(sudoku: Sudoku, row: int, col: int) -> bool:
    """
    Preenche o Sudoku recursivamente com uma solução válida
    
    Args:
        sudoku: Instância do Sudoku
        row: Linha atual
        col: Coluna atual
        
    Returns:
        True se conseguiu preencher, False caso contrário
    """
    if row == sudoku.size:
        return True
    
    next_row = row + 1 if col == sudoku.size - 1 else row
    next_col = 0 if col == sudoku.size - 1 else col + 1
    
    # Números embaralhados para adicionar aleatoriedade
    numbers = list(range(1, sudoku.size + 1))
    random.shuffle(numbers)
    
    for num in numbers:
        if sudoku.is_valid(row, col, num):
            sudoku.grid[row][col] = num
            if fill_sudoku(sudoku, next_row, next_col):
                return True
            sudoku.grid[row][col] = 0
    
    return False

def generate_sudoku(size: int, empty_cells: int) -> Sudoku:
    """
    Gera um puzzle de Sudoku válido com número específico de células vazias
    
    Args:
        size: Tamanho do Sudoku (3, 6 ou 9)
        empty_cells: Número de células vazias desejado
        
    Returns:
        Instância de Sudoku gerada
    """

    # gera um sudoku e preenche com uma solução válida, depois usamos um algoritmo fisher yates para remover células aleatoriamente
    # ele da shuffle nas posicoes do array e remove de acordo com o numero que é pra remover

    sudoku = Sudoku(size)
    
    # Preenche o Sudoku com uma solução válida
    fill_sudoku(sudoku, 0, 0)
    
    # Remove células aleatoriamente
    total_cells = size * size
    positions = list(range(total_cells))
    random.shuffle(positions)
    
    cells_to_remove = min(empty_cells, total_cells)
    
    for i in range(cells_to_remove):
        pos = positions[i]
        row = pos // size
        col = pos % size
        sudoku.grid[row][col] = 0
    
    return sudoku
