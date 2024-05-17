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

piece_types = {
    "F": ("FC", "FD", "FB", "FE"),
    "B": ("BC", "BD", "BB", "BE"),
    "V": ("VC", "VD", "VB", "VE"),
    "L": ("LH", "LV")
}

piece_to_bin = {
    "FC": (True, False, False, False), "FB": (False, False, True, False), "FE": (False, False, False, True), "FD": (False, True, False, False),
    "BC": (True, True, False, True), "BB": (False, True, True, True), "BE": (True, False, True, True), "BD": (True, True, True, False),
    "VC": (True, False, False, True), "VB": (False, True, True, False), "VE": (False, False, True, True), "VD": (True, True, False, False),
    "LH": (False, True, False, True), "LV": (True, False, True, False)
}

bin_to_piece = {
    (True, False, False, False): "FC", (False, False, True, False): "FB", (False, False, False, True): "FE", (False, True, False, False): "FD",
    (True, True, False, True): "BC", (False, True, True, True): "BB", (True, False, True, True): "BE", (True, True, True, False): "BD",
    (True, False, False, True): "VC", (False, True, True, False): "VB", (False, False, True, True): "VE", (True, True, False, False): "VD",
    (False, True, False, True): "LH", (True, False, True, False): "LV"
}

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
    def __init__(self, grid, moved):
        self.grid = grid
        self.size = len(grid)
        self.moved = moved
    
    def valid_coord(self, row: int, col: int) -> bool:
        """Devolve True sse (row, col) é uma coordenada válida do tabuleiro."""
        return (0 <= row <= self.size - 1 and 0 <= col <= self.size - 1)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.valid_coord(row, col):
            return bin_to_piece[tuple(self.grid[row][col])]
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
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))
    
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
    
    def get_next_piece(self):
        # obter coordenadas de peça que não esteja locked
        pass

    def match_pieces(self, row: int, col: int, direction: int):
        if direction % 2 == 1:
            return self.grid[row][col][direction] and self.grid[row][col - (direction - 2)][(direction + 2) % 4]
        else:
            return self.grid[row][col][direction] and self.grid[row + (direction - 1)][col][(direction + 2) % 4]
        

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        grid, moved = [], []

        line = stdin.readline().split()
        while len(line) != 0:
            grid.append(np.array([piece_to_bin[piece] for piece in line]))
            moved.append(np.array([False for piece in line]))
            line = stdin.readline().split()
        
        grid_np = np.array(grid)
        moved_np = np.array(moved)
        board = Board(grid_np, moved_np)
        board.filterActions()

        return board
    
    
    def fix_corners(self):
        top_left, top_right = self.get_type(0, 0), self.get_type(0, self.size - 1)
        bottom_left, bottom_right = self.get_type(self.size - 1, 0), self.get_type(self.size - 1, self.size - 1)

        if top_left == "V":
            self.grid[0][0] = np.array((0, 1, 1, 0))
            self.moved[0][0] = True
        
        if top_right == "V":
            self.grid[0][self.size - 1] = np.array((0, 0, 1, 1))
            self.moved[0][self.size - 1] = True
        
        if bottom_right == "V":
            self.grid[self.size - 1][self.size - 1] = np.array((1, 0, 0, 1))
            self.moved[self.size - 1][self.size - 1] = True
        
        if bottom_left == "V":
            self.grid[self.size - 1][0] = np.array((1, 1, 0, 0))
            self.moved[self.size - 1][0] = True
    
    def fix_borders(self):
        # Fix top
        for col in range(1, self.size - 1):
            piece_type = self.get_type(0, col)

            if piece_type == "B":
                self.grid[0][col] = np.array((0, 1, 1, 1))
                self.moved[0][col] = True
            elif piece_type == "L":
                self.grid[0][col] = np.array((0, 1, 0, 1))
                self.moved[0][col] = True
        
        # Fix bottom
        for col in range(1, self.size - 1):
            piece_type = self.get_type(self.size - 1, col)

            if piece_type == "B":
                self.grid[self.size - 1][col] = np.array((1, 1, 0, 1))
                self.moved[self.size - 1][col] = True
            elif piece_type == "L":
                self.grid[self.size - 1][col] = np.array((0, 1, 0, 1))
                self.moved[self.size - 1][col] = True
        
        # Fix left
        for line in range(1, self.size - 1):
            piece_type = self.get_type(line, 0)

            if piece_type == "B":
                self.grid[line][0] = np.array((1, 1, 1, 0))
                self.moved[line][0] = True
            elif piece_type == "L":
                self.grid[line][0] = np.array((1, 0, 1, 0))
                self.moved[line][0] = True

        # Fix right
        for line in range(1, self.size - 1):
            piece_type = self.get_type(line, self.size - 1)

            if piece_type == "B":
                self.grid[line][self.size - 1] = np.array((1, 0, 1, 1))
                self.moved[line][self.size - 1] = True
            elif piece_type == "L":
                self.grid[line][self.size - 1] = np.array((1, 0, 1, 0))
                self.moved[line][self.size - 1] = True


    
    def filterActions(self):
        self.fix_corners()
        self.fix_borders()
        
    
    def print(self):
        string = ""
        for i in range(0, self.size):
            for j in range(0, self.size):
                if j == self.size - 1 and i != self.size - 1:
                    string += self.get_value(i, j) + "\n"
                else:
                    if i == self.size - 1 and j == self.size - 1:
                        string += self.get_value(i, j)
                    else:
                        string += self.get_value(i, j) + "\t" 
        return string

    # TODO: outros metodos da classe

    #"""
    def get_adjancent_list(self, row: int, col: int):
        lista_adj = np.array((None, None, None, None))
        
        for i in range(0, 4):
            if i % 2 == 0:
                a = row + (i - 1)
                if self.valid_coord(a, col):
                    if self.moved[a][col]:
                        lista_adj[i] = self.grid[a][col][(i + 2) % 4]
                else:
                    lista_adj[i] = False
            else:
                b = col - (i - 2)
                if self.valid_coord(row, b):
                    if self.moved[row][b]:
                        lista_adj[i] = self.grid[row][b][(i + 2) % 4]
                else:
                    lista_adj[i] = False
                    
        lista_adj_np = np.array(lista_adj)
        return lista_adj
    #"""
    
    """
    def get_adjancent_list(self, row: int, col: int):
        lista_adj = [None, None, None, None]
        directions = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]

        for i, (r, c) in enumerate(directions):
            if self.valid_coord(r, c):
                if self.moved[r][c]:
                    lista_adj[i] = self.grid[r][c][(i + 2) % 4]
            else:
                lista_adj[i] = False

        return np.array(lista_adj)
    """

    
    def possible_actions(self, lista, piece_type: str):
        possible = []
        if piece_type == "L":
            number = 2
        else:
            number = 4
        for i in range(0, number):
            for j in range(0,4):
                if lista[j] != None:
                    if piece_to_bin[piece_types[piece_type][i]][j] != lista[j]:
                        break
                if j == 3:
                    possible.append(piece_to_bin[piece_types[piece_type][i]])
        return possible
    


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        initial_state = PipeManiaState(board)
        super().__init__(initial_state)
        pass

    
    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a partir do estado passado como argumento."""
        board = state.board
        grid = board.grid
        moved = board.moved
        size = len(grid)
        
        best_action_list = None
        min_actions = float('inf')
        
        for i in range(size):
            for j in range(size):
                if not moved[i][j]:
                    lista_adj = board.get_adjancent_list(i, j)
                    piece_type = board.get_type(i, j)
                    possible = board.possible_actions(lista_adj, piece_type)
                    action_list = [(i, j, action) for action in possible]

                    if len(action_list) == 1:
                        return action_list
                    
                    if len(action_list) < min_actions:
                        min_actions = len(action_list)
                        best_action_list = action_list

        return best_action_list if best_action_list is not None else []


    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, orientation) = action
        board = state.board
        new_grid = np.copy(board.grid)
        new_moved = np.copy(board.moved)
        new_grid[row][col] = np.array(orientation)
        new_moved[row][col] = True
        new_board = Board(new_grid, new_moved)

        def update_adjacent_piece(new_board, row, col):
            if new_board.valid_coord(row, col) and not new_board.moved[row][col]:
                lista_adj = new_board.get_adjancent_list(row, col)
                piece_type = new_board.get_type(row, col)
                possible = new_board.possible_actions(lista_adj, piece_type)

                # Se há apenas uma ação possível, atualize a peça
                if len(possible) == 1:
                    new_board.grid[row][col] = np.array(possible[0])
                    new_board.moved[row][col] = True

        # Verifique as peças adjacentes
        adjacent_positions = [
            (row - 1, col),  # acima
            (row + 1, col),  # abaixo
            (row, col - 1),  # à esquerda
            (row, col + 1)   # à direita
        ]

        for adj_row, adj_col in adjacent_positions:
            update_adjacent_piece(new_board, adj_row, adj_col)

        return PipeManiaState(new_board)



    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        size = board.size
        visited = set()
        stack = [(0, 0)]

        def is_valid_and_match(row, col, direction):
            if direction == 1:
                adj_row, adj_col = row, col + 1
            elif direction == 3:
                adj_row, adj_col = row, col - 1
            elif direction == 2:
                adj_row, adj_col = row + 1, col
            elif direction == 0:
                adj_row, adj_col = row - 1, col
            else:
                return False
            
            return (
                board.valid_coord(adj_row, adj_col) and 
                board.match_pieces(row, col, direction)
            )

        while stack:
            row, col = stack.pop()  # Obter a próxima posição a ser explorada
            if (row, col) in visited:
                continue  # Evitar ciclos
            visited.add((row, col))

            for direction in [0, 1, 2, 3]:
                if board.grid[row][col][direction]:
                    if not is_valid_and_match(row, col, direction):
                        return False
                    adj_row, adj_col = (
                        (row, col + 1) if direction == 1 else
                        (row, col - 1) if direction == 3 else
                        (row + 1, col) if direction == 2 else
                        (row - 1, col)
                    )
                    if (adj_row, adj_col) not in visited and board.valid_coord(adj_row, adj_col):
                        stack.append((adj_row, adj_col))

        # Verificar se todas as posições foram visitadas
        return len(visited) == size * size


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
    goal = depth_first_tree_search(pipe)

    print(goal.state.board.print())
    #"""