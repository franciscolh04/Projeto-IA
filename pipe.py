from sys import stdin

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:
    """ Representação interna de uma grelha de PipeMania. """
    def __init__(self, grid):
        self.grid = grid
        self.n = len(grid)

 
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row not in (0, self.n - 1):
            return (self.grid[row - 1][col], self.grid[row + 1][col])
        elif row == 0:
            return (None, self.grid[row + 1][col])
        elif row == self.n - 1:
            return (self.grid[row - 1][col], None)
        else:
            return (None, None)


    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        if col not in (0, self.n - 1):
            return (self.grid[row][col - 1], self.grid[row][col + 1])
        elif col == 0:
            return (None, self.grid[row][col + 1])
        elif col == self.n - 1:
            return (self.grid[row][col - 1], None)
        else:
            return (None, None)

    
    def get_value(self, row: int, col: int) -> (str):
        """ Devolve o valor preenchido na posição especificada."""
        if 0 <= row <= self.n - 1 and 0 <= col <= self.n - 1:
            return self.grid[row][col]
        else:
            return None

    def __str__(self):
        string = ""
        for i in range(0, self.n):
            for j in range(0, self.n):
                if j == self.n - 1:
                    string += self.grid[i][j] + "\n"
                else:
                    string += self.grid[i][j] + " " #verificar se é espaço ou tabulação
        return string


    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe_mania.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        grid = []

        line = stdin.readline().split()
        while len(line) != 0:
            grid.append(line)
            line = stdin.readline().split()

        #tabuleiro = Board(grid)
        #print(tabuleiro)

        return Board(grid)

# Exemplo 1:
# Ler grelha do figura 1a:
board = Board.parse_instance()
print(board.adjacent_vertical_values(0, 0))
print(board.adjacent_horizontal_values(0, 0))
print(board.adjacent_vertical_values(1, 1))
print(board.adjacent_horizontal_values(1, 1))