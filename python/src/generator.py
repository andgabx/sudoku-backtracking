from sudoku import Sudoku

# Gerador Linear Congruential Generator (LCG) portável
# Usa os mesmos parâmetros que C para garantir compatibilidade
class PortableLCG:
    def __init__(self, seed=0):
        self.state = seed & 0x7fffffff
    
    def next(self):
        # LCG: (a * state + c) mod m
        # Parâmetros do Python 3.2+ (usado por random.randint)
        # a = 1103515245, c = 12345, m = 2^31
        self.state = (1103515245 * self.state + 12345) & 0x7fffffff
        return self.state

# Instância global do LCG
_lcg = None

def _lcg_seed(seed):
    global _lcg
    _lcg = PortableLCG(seed)

def _lcg_next():
    return _lcg.next()

def _shuffle_portable(array):
    """Shuffle usando LCG portável (compatível com C)"""
    n = len(array)
    for i in range(n - 1, 0, -1):
        j = _lcg_next() % (i + 1)
        array[i], array[j] = array[j], array[i]

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
    _shuffle_portable(numbers)  # Usa LCG portável em vez de random.shuffle
    
    for num in numbers:
        if sudoku.is_valid(row, col, num):
            sudoku.grid[row][col] = num
            if fill_sudoku(sudoku, next_row, next_col):
                return True
            sudoku.grid[row][col] = 0
    
    return False

def generate_sudoku(size: int, empty_cells: int, seed: int = None) -> Sudoku:
    """
    Gera um puzzle de Sudoku válido com número específico de células vazias
    
    Args:
        size: Tamanho do Sudoku (3, 6 ou 9)
        empty_cells: Número de células vazias desejado
        seed: (opcional) Seed para o gerador aleatório
        
    Returns:
        Instância de Sudoku gerada
    """

    # gera um sudoku e preenche com uma solução válida, depois usamos um algoritmo fisher yates para remover células aleatoriamente
    # ele da shuffle nas posicoes do array e remove de acordo com o numero que é pra remover

    if seed is not None:
        _lcg_seed(seed)  # Usa LCG portável em vez de random.seed
    else:
        import random
        _lcg_seed(random.randint(0, 2**31-1))  # Inicializa com seed aleatória se não fornecida
    
    sudoku = Sudoku(size)
    
    # Preenche o Sudoku com uma solução válida
    fill_sudoku(sudoku, 0, 0)
    
    # Remove células aleatoriamente
    total_cells = size * size
    positions = list(range(total_cells))
    _shuffle_portable(positions)  # Usa LCG portável em vez de random.shuffle
    
    cells_to_remove = min(empty_cells, total_cells)
    
    for i in range(cells_to_remove):
        pos = positions[i]
        row = pos // size
        col = pos % size
        sudoku.grid[row][col] = 0
    
    return sudoku
