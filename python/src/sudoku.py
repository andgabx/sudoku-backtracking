
"""
Módulo para representação e operações básicas do Sudoku
"""
import math
from typing import List, Optional, Tuple

class Sudoku:
    """Classe para representar um tabuleiro de Sudoku"""
    
    def __init__(self, size: int):
        """
        Inicializa um Sudoku vazio
        
        Args:
            size: Tamanho do grid (3, 6 ou 9)
        """
        self.size = size
        self.box_size = int(math.sqrt(size))
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Verifica se é válido colocar um número em uma posição
        
        Args:
            row: Linha
            col: Coluna
            num: Número a ser colocado
            
        Returns:
            True se válido, False caso contrário
        """
        # Verifica linha
        if num in self.grid[row]:
            return False
        
        # Verifica coluna
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False
        
        # Verifica caixa
        box_start_row = row - row % self.box_size
        box_start_col = col - col % self.box_size
        
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.grid[box_start_row + i][box_start_col + j] == num:
                    return False
        
        return True
    
    def find_empty_cell(self) -> Optional[Tuple[int, int]]:
        """
        Encontra a próxima célula vazia (com valor 0)
        
        Returns:
            Tupla (row, col) da célula vazia, ou None se não houver
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None
    
    def count_empty_cells(self) -> int:
        """
        Conta o número de células vazias
        
        Returns:
            Número de células vazias
        """
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    count += 1
        return count
    
    def copy(self) -> 'Sudoku':
        """
        Cria uma cópia do Sudoku
        
        Returns:
            Nova instância de Sudoku com os mesmos valores
        """
        new_sudoku = Sudoku(self.size)
        for i in range(self.size):
            for j in range(self.size):
                new_sudoku.grid[i][j] = self.grid[i][j]
        return new_sudoku
    
    def print(self):
        """Imprime o Sudoku formatado"""
        for i in range(self.size):
            if i % self.box_size == 0 and i != 0:
                print("-" * (self.size * 2 + self.box_size - 1))
            
            for j in range(self.size):
                if j % self.box_size == 0 and j != 0:
                    print("| ", end="")
                print(f"{self.grid[i][j]} ", end="")
            print()
