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
    depth_limited_search,
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
    
    def valid_coord(self, row: int, col: int) -> bool:
        """Devolve True sse (row, col) é uma coordenada válida do tabuleiro."""
        return (0 <= row <= self.size - 1 and 0 <= col <= self.size - 1)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.valid_coord(row, col):
            return self.grid[row][col][0]
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
    
    def is_locked(self, row: int, col: int) -> bool:
        if self.valid_coord(row, col):
            return self.grid[row][col][1]
        else:
            return None
    
    def lock_piece(self, row: int, col: int):
        if self.valid_coord(row, col):
            self.grid[row][col][1] = True

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))
    
    def rotate_piece(self, row: int, col: int, clockwise: bool):
        """Devolve uma nova instância da classe Board com a
        rotação aplicada."""
        all_orientations = ('C', 'D', 'B', 'E')
        dic_volta = {'H': 'V', 'V': 'H'}

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
            new_value += piece_type + dic_volta[orientation]
        
        new_grid = self.grid
        new_grid[row][col][0] = new_value

        return Board(new_grid)
    
    def set_orientation(self, row: int, col: int, new_orientation: str):
        """Devolve uma nova instância da classe Board com a peça na
        orientação especificada."""
        if self.get_orientation(row, col) == new_orientation:
            return self
        else:
            new_value = self.get_type(row, col) + new_orientation
            new_grid = self.grid
            new_grid[row][col][0] = new_value

            return Board(new_grid)
    
    def get_sides_to_connect(self, row: int, col: int) -> tuple:
        """Devolve um tuplo com as orientações possíveis para as peças
        adjacentes à peça espeficicada"""
        dic = {'FC': ('B', 'V'), 'FB': ('C', 'V'), 'FE':('D', 'H'), 'FD':('E', 'H'),
               'BC': ('D', 'E', 'H', 'B', 'V'), 'BB': ('D', 'E', 'H', 'C', 'V'),
               'BE': ('D', 'H', 'C', 'B', 'V'), 'BD': ('E', 'H', 'C', 'B', 'V'),
               'VC': ('D', 'H', 'B', 'V'), 'VB': ('E', 'H', 'C', 'V'),
               'VE': ('D', 'H', 'C', 'V'), 'VD': ('E', 'H', 'B', 'V'),
               'LH': ('D', 'E', 'H'), 'LV': ('B', 'C', 'V')}
        
        return dic[self.get_value(row, col)]
    
    def get_next_piece(self):
        # resolver o que der nos cantos
        # resolver o que der nas bordas
        # obter coordenadas de peça que não esteja locked
        pass

    def get_possible_moves(self, row: int, col: int):
        # obter possíveis posições para a peça especificada tendo em conta as suas adjacentes
        pass
    
    def get_connection_right(self, row: int, col: int) -> bool:
        orientation = self.get_orientation(row, col)
        if orientation in ("D", "H"):
            return True
        piece = self.get_value(row, col)
        if piece in ("BC", "BB", "VB"):
            return True
        else: 
            return False
    
    def get_connection_left(self, row: int, col: int) -> bool:
        orientation = self.get_orientation(row, col)
        if orientation in ("E", "H"):
            return True
        piece = self.get_value(row, col)
        if piece in ("BC", "BB", "VC"):
            return True
        else: 
            return False
    
    def get_connection_top(self, row: int, col: int) -> bool:
        orientation = self.get_orientation(row, col)
        if orientation in ("C", "V"):
            return True
        piece = self.get_value(row, col)
        if piece in ("BE", "BD", "VD") :
            return True
        else: 
            return False

    def get_connection_bottom(self, row: int, col: int) -> bool:
        orientation = self.get_orientation(row, col)
        if orientation in ("B", "V"):
            return True
        piece = self.get_value(row, col)
        if piece in ("BE", "BD", "VE") :
            return True
        else: 
            return False

    def match_pieces(self, row: int, col: int, direction: str):
        if direction == "r":
            connect_1 = self.get_connection_right(row,col)
            connect_2 = self.get_connection_left(row,col + 1)
        elif direction == "l":
            connect_1 = self.get_connection_right(row,col - 1)
            connect_2 = self.get_connection_left(row,col)
        elif direction == "b":
            connect_1 = self.get_connection_bottom(row,col)
            connect_2 = self.get_connection_top(row + 1,col)
        elif direction == "t":
            connect_1 = self.get_connection_bottom(row - 1,col)
            connect_2 = self.get_connection_top(row,col)
    
        return connect_1 and connect_2
            


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
            grid.append([[piece, False, []] for piece in line])
            line = stdin.readline().split()
        
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                piece = grid[i][j][0]
                if piece[0] != "L":
                    grid[i][j][2] = [(i, j, "C"), (i, j, "B"), (i, j, "E"), (i, j, "D")]
                else:
                    grid[i][j][2] = [(i, j, "H"), (i, j, "V")]
        
        board = Board(grid)
        board.filterActions()
        print(grid)

        return board
    
    def fix_corners(self):
        top_left, top_right = self.get_type(0, 0), self.get_type(0, self.size - 1)
        bottom_left, bottom_right = self.get_type(self.size - 1, 0), self.get_type(self.size - 1, self.size - 1)

        if top_left == "V":
            self.grid[0][0][2] = [(0, 0, "B")]
        elif top_left == "F":
            self.grid[0][0][2] = [(0, 0, "B"), (0, 0, "D")]
        
        if top_right == "V":
            self.grid[0][self.size - 1][2] = [(0, self.size - 1, "E")]
        elif top_right == "F":
            self.grid[0][self.size - 1][2] = [(0, self.size - 1, "E"), (0, self.size - 1, "B")]
        
        if bottom_right == "V":
            self.grid[self.size - 1][self.size - 1][2] = [(self.size - 1, self.size - 1, "C")]
        elif bottom_right == "F":
             self.grid[self.size - 1][self.size - 1][2] = [(self.size - 1, self.size - 1, "C"), (self.size - 1, self.size - 1, "E")]
        
        if bottom_left == "V":
            self.grid[self.size - 1][0][2] = [(self.size - 1, 0, "D")]
        elif bottom_left == "F":
            self.grid[self.size - 1][0][2] = [(self.size - 1, 0, "D"), (self.size - 1, 0, "C")]
    
    def fix_borders(self):
        # Fix top
        for col in range(1, self.size - 1):
            piece_type = self.get_type(0, col)

            if piece_type == "V":
                self.grid[0][col][2] = [(0, col, "B"), (0, col, "E")]
            elif piece_type == "F":
                self.grid[0][col][2] = [(0, col, "B"), (0, col, "E"), (0, col, "D")]
            elif piece_type == "B":
                self.grid[0][col][2] = [(0, col, "B")]
            elif piece_type == "L":
                self.grid[0][col][2] = [(0, col, "H")]
        
        # Fix bottom
        for col in range(1, self.size - 1):
            piece_type = self.get_type(self.size - 1, col)

            if piece_type == "V":
                self.grid[self.size - 1][col][2] = [(self.size - 1, col, "C"), (self.size - 1, col, "D")]
            elif piece_type == "F":
                self.grid[self.size - 1][col][2] = [(self.size - 1, col, "C"), (self.size - 1, col, "E"), (self.size - 1, col, "D")]
            elif piece_type == "B":
                self.grid[self.size - 1][col][2] = [(self.size - 1, col, "C")]
            elif piece_type == "L":
                self.grid[self.size - 1][col][2] = [(self.size - 1, col, "H")]
        
        # Fix left
        for line in range(1, self.size - 1):
            piece_type = self.get_type(line, 0)

            if piece_type == "V":
                self.grid[line][0][2] = [(line, 0, "B"), (line, 0, "D")]
            elif piece_type == "F":
                self.grid[line][0][2] = [(line, 0, "B"), (line, 0, "C"), (line, 0, "D")]
            elif piece_type == "B":
                self.grid[line][0][2] = [(line, 0, "D")]
            elif piece_type == "L":
                self.grid[line][0][2] = [(line, 0, "V")]

        # Fix right
        for line in range(1, self.size - 1):
            piece_type = self.get_type(line, self.size - 1)

            if piece_type == "V":
                self.grid[line][self.size - 1][2] = [(line, self.size - 1, "E"), (line, self.size - 1, "C")]
            elif piece_type == "F":
                self.grid[line][self.size - 1][2] = [(line, self.size - 1, "B"), (line, self.size - 1, "C"), (line, self.size - 1, "E")]
            elif piece_type == "B":
                self.grid[line][self.size - 1][2] = [(line, self.size - 1, "E")]
            elif piece_type == "L":
                self.grid[line][self.size - 1][2] = [(line, self.size - 1, "V")]


    
    def filterActions(self):
        self.fix_corners()
        self.fix_borders()
        
    
    def print(self):
        string = ""
        for i in range(0, self.size):
            for j in range(0, self.size):
                if j == self.size - 1:
                    string += self.get_value(i, j) + "\n"
                else:
                    string += self.get_value(i, j) + " " #verificar se é espaço ou tabulação
        return string

    def deepcopy(self):
        # Criando uma nova matriz vazia com as mesmas dimensões do tabuleiro original
        new_grid = [[[None, False, []] for _ in range(board.size)] for _ in range(board.size)]
        
        # Copiando os elementos e atributos do tabuleiro original para o novo tabuleiro
        for i in range(board.size):
            for j in range(board.size):
                piece, locked, connections = self.grid[i][j]
                new_grid[i][j] = [piece, locked, self.deepcopy_list(connections)]  # Usando copy para criar uma cópia da lista de conexões
        
        # Criando um novo objeto Board com a nova matriz
        new_board = Board(new_grid)
        return new_board
    
    def deepcopy_list(self, lst):
        if not isinstance(lst, list):
            return lst  # Se o elemento não for uma lista, apenas o retorna
        else:
            return [self.deepcopy_list(item) for item in lst]  # Caso contrário, faz uma cópia profunda de cada elemento


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
        action_list = []
        grid = state.board.grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                for action in grid[i][j][2]:
                    action_list.append(action)
        return action_list
        # TODO
        # obter próxima peça
        # obter lista de ações possíveis para peça
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, orientation) = action
        board = state.board

        action_list = board.deepcopy_list(board.grid[row][col][2])
        #print("action list " + str((row, col)) + ": " + str(action_list))
        action_list.remove(action)

        new_board = board.deepcopy()
        new_board.grid[row][col][2] = action_list
        if len(action_list) == 0:
            new_board.lock_piece(row, col)
        new_board.set_orientation(row, col, orientation)

        return PipeManiaState(new_board)
        #"""


    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        size = board.size
        visited = set()  # Conjunto para armazenar as posições visitadas

        stack = [(0, 0)]  # Iniciar a pilha com a posição inicial (0, 0)

        while stack:
            row, col = stack.pop()  # Obter a próxima posição a ser explorada
            if (row, col) in visited:
                continue  # Evitar ciclos
            visited.add((row, col))
            print("row, col: " + str((row, col)))

            # Verificar se a peça atual está corretamente conectada
            left_piece, right_piece = board.adjacent_horizontal_values(row, col)
            top_piece, bottom_piece = board.adjacent_vertical_values(row, col)
            match_right = match_left = match_bottom = match_top = True
            if board.get_connection_right(row, col):
                print("direita")
                match_right = board.match_pieces(row, col, "r")
                if match_right and (row, col + 1) not in visited:
                    stack.append((row, col + 1))
            if board.get_connection_left(row, col):
                print("esquerda")
                match_left = board.match_pieces(row, col, "l")
                if match_left and (row, col - 1) not in visited:
                    stack.append((row, col - 1))
            if board.get_connection_bottom(row, col):
                print("baixo")
                match_bottom = board.match_pieces(row, col, "b")
                if match_bottom and (row + 1, col) not in visited:
                    stack.append((row + 1, col))
            if board.get_connection_top(row, col):
                print("cima")
                match_top = board.match_pieces(row, col, "t")
                if match_top and (row - 1, col) not in visited:
                    stack.append((row - 1, col))
            
            if not (match_left and match_right and match_bottom and match_top):
                return False 
    
        print(visited)        
                    
        for i in range(size):
            for j in range(size):
                if (i, j) not in visited:
                    return False

        return True


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
    #"""
    board = Board.parse_instance()
    pipe = PipeMania(board)
    goal = breadth_first_tree_search(pipe)
    print(goal.state.board.print())
    #"""

    """
    board = Board.parse_instance()
    pipe = PipeMania(board)
    state = PipeManiaState(board)
    print("Goal test: ")
    print(pipe.goal_test(state))
    #"""

    """
    board = Board.parse_instance()
    print(board.get_sides_to_connect(1, 0))
    print(board.get_sides_to_connect(1, 2))
    board.set_orientation(1, 0, "B")
    board.set_orientation(1, 2, "H")
    print(board.get_sides_to_connect(1, 0))
    print(board.get_sides_to_connect(1, 2))
    """


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

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(s5))
    print("Is goal?", problem.goal_test(s11))
    print("Solution s5:\n", s5.board.print(), sep="")
    print("Solution s11:\n", s11.board.print(), sep="")
    #"""