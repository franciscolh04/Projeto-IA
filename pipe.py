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
    
    def get_type(self, row: int, col: int) -> str:
        """Devolve o tipo da peça na respetiva posição do tabuleiro."""
        piece_type = self.get_value(row, col)
        return piece_type[0] if piece_type is not None else None
    
    def get_orientation(self, row: int, col: int) -> str:
        """Devolve a orientação da peça na respetiva posição do tabuleiro."""
        orientation = self.get_value(row, col)
        return orientation[1] if orientation is not None else None

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
    
    def set_value(self, row: int, col: int, clockwise: bool):
        """Devolve uma nova instância da classe Board com a
        alteração aplicada"""
        all_orientations = ('C', 'D', 'B', 'E')
        dic = {'H': 'V', 'V': 'H'}

        #print("Value: " + self.get_value(row, col))

        piece_type = self.get_type(row, col)
        orientation = self.get_orientation(row, col)
        current_orientation = all_orientations.index(orientation)
        new_value = ''

        if piece_type in ('F', 'B', 'V'):
            if clockwise:
                new_value += piece_type + all_orientations[(current_orientation + 1) % 4]
            else:
                new_value += piece_type + all_orientations[(current_orientation - 1) % 4]
        else:
            new_value += piece_type + dic[orientation]
        
        new_grid = self.grid
        new_grid[row][col] = new_value

        #print(self.get_value(row, col))
        #print("new: " + new_value)

        return Board(new_grid)


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
    
    def print(self):
        string = ""
        for i in range(0, self.size):
            for j in range(0, self.size):
                if j == self.size - 1:
                    string += self.grid[i][j] + "\n"
                else:
                    string += self.grid[i][j] + " " #verificar se é espaço ou tabulação
        return string

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        initial_state = PipeManiaState(board)
        super().__init__(initial_state)
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
        (row, col, direction) = action
        return PipeManiaState(state.board.set_value(row, col, direction))

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

    """
    #Exemplo 1
    board = Board.parse_instance()
    print(board.adjacent_vertical_values(0, 0))
    print(board.adjacent_horizontal_values(0, 0))
    print(board.adjacent_vertical_values(1, 1))
    print(board.adjacent_horizontal_values(1, 1))
    #print(board.get_type(0, 1))
    #print(board.get_orientation(0, 1))
    """

    """
    #Exemplo 2
    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Criar um estado com a configuração inicial:
    initial_state = PipeManiaState(board)
    # Mostrar valor na posição (2, 2):
    print(initial_state.board.get_value(2, 2))
    # Realizar ação de rodar 90° clockwise a peça (2, 2)
    result_state = problem.result(initial_state, (2, 2, True))
    # Mostrar valor na posição (2, 2):
    print(result_state.board.get_value(2, 2))
    """

    #Exemplo 3
    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Criar um estado com a configuração inicial:
    s0 = PipeManiaState(board)
    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (0, 1, True))
    s2 = problem.result(s1, (0, 1, True))
    s3 = problem.result(s2, (0, 2, True))
    s4 = problem.result(s3, (0, 2, True))
    s5 = problem.result(s4, (1, 0, True))
    s6 = problem.result(s5, (1, 1, True))
    s7 = problem.result(s6, (2, 0, False)) # anti-clockwise (exemplo de uso)
    s8 = problem.result(s7, (2, 0, False)) # anti-clockwise (exemplo de uso)
    s9 = problem.result(s8, (2, 1, True))
    s10 = problem.result(s9, (2, 1, True))
    s11 = problem.result(s10, (2, 2, True))

    print("Solution:\n", s11.board.print(), sep="")