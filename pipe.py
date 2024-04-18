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
    def __init__(self,grid):
        self.grid = grid
        pass

 
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        return (self.grid[row - 1][col], self.grid[row + 1][col])
        #falta verificações
        
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """ Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        return (self.grid[row][col - 1], self.grid[row][col + 1])
        #falta verificações

        pass
    
    # TODO: outros metodos da classe

    @staticmethod
    def parse_instance():
        """Lê a instância do problema do standard input (stdin)
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe_mania.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        grid = []

        line = stdin.readline().split()
        while len(line) != 0:
            grid.append(line)
            line = stdin.readline().split()
        
        Board(grid)
        return grid

board = Board.parse_instance()
print(board.grid)