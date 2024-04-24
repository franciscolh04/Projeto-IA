# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 106494 Mafalda Szolnoky Ramos Pinto Dias
# 106970 Francisco Lourenço Heleno

from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
    
    # ?TODO?: get_row and get_col

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row <= self.size - 1 and 0 <= col <= self.size - 1:
            return self.grid[row][col]
        else:
            return None

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        """
        if row not in (0, self.size - 1):
            return (self.grid[row - 1][col], self.grid[row + 1][col])
        elif row == 0:
            return (None, self.grid[row + 1][col])
        elif row == self.size - 1:
            return (self.grid[row - 1][col], None)
        else:
            return (None, None)
        """
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        """
        if col not in (0, self.size - 1):
            return (self.grid[row][col - 1], self.grid[row][col + 1])
        elif col == 0:
            return (None, self.grid[row][col + 1])
        elif col == self.size - 1:
            return (self.grid[row][col - 1], None)
        else:
            return (None, None)
        """
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        grid = []

        line = stdin.readline().split()
        while len(line) != 0:
            grid.append(line)
            line = stdin.readline().split()

        # tabuleiro = Board(grid)
        # print(tabuleiro)

        return Board(grid)

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    print(board.adjacent_vertical_values(0, 0))
    print(board.adjacent_horizontal_values(0, 0))
    print(board.adjacent_vertical_values(1, 1))
    print(board.adjacent_horizontal_values(1, 1))