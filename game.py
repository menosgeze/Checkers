from elements import Piece, Cell, Board

class Game:
    def __init__(self, starter):
        self.turn = 0
        if starter.lower() == 'red':
            self.order = ['red', 'black']
            self.direction = [1, -1]
        else:
            self.order = ['black', 'red']
            self.direction = [-1, 1]        
        
        self.board = Board()
        
    def piece_options(
        self, piece,
        row_ind, col_ind,
        only_jumps = False,
        options = [],
        root = []
    ):
        options = []
        
        # possible left movement.
        next_row = row_ind + self.direction[self.turn]
        # i = -1 is left, and i = 1 is right.
        
        if not only_jumps:
            for i in [-1, 1]:
                # testing for single move.
                if (
                    col_ind + i in range(8) and
                    self.board.board[next_row][col_ind + i].piece is None
                ):
                    options.append(
                        [row_ind, col_ind, next_row, col_ind + i])
        
        # single jump iterated.
        for i in [-1, 1]:
            next_next_row = next_row = self.direction[self.turn]
            if (
                col_ind + i in range(8)
                and
                self.board.board[next_row][col_ind + i].piece is not None
                and
                self.board.board[next_row][col_ind + i].piece._color == self.order[(self.turn + 1) % 2]
                and
                self.board.board[next_next_row][col_ind + 2 * i].piece is None
            ):
                options.append(
                    root + [row_ind, col_ind, next_next_row, col_ind + 2 * i])
                continue_jumping = self.piece_options(
                    piece,
                    next_next_row, col_ind + 2 * i,
                    only_jumps=True,
                    options=options,
                    root=root + [row_ind, col_ind, next_next_row, col_ind + 2 * i] 
                )
                if len(continue_jumping):
                    options += continue_jumping
        return options


    def turn_options(self):
        options = []
        for row_index in range(8):
            for col_index in range(8):
                piece = self.board.board[row_index][col_index].piece
                if (
                    piece is not None
                    and piece._color == self.order[self.turn]
                ):
                    options += self.piece_options(piece, row_index, col_index)
        jump_options = [
            opt for opt in options
            if (opt[0] - opt[-2]) % 2 == 0]

        if len(jump_options):
            options = jump_options

        for opt in options:
            print(options.index(opt), opt)
        self.list_of_moves = options
        return options

    def choose_turn(self):
        while True:
            try:
                turn_choice = int(input("Choose your turn by index: "))
                assert turn_choice in range(len(self.list_of_moves))
                print(
                    f"Player selected turn {turn_choice} "
                    f"turn {self.list_of_moves[int(turn_choice)]}.")
                return turn_choice
            except:
                print('That is not a valid option')
        
    def take_turn(self):
        options = self.turn_options()
        turn_choice = self.list_of_moves[self.choose_turn()]
        is_jump = (turn_choice[0] - turn_choice[-2]) % 2 == 0
        if not is_jump:
            piece = self.board.board[turn_choice[0]][turn_choice[1]].piece
            self.board.board[turn_choice[0]][turn_choice[1]].piece = None
            self.board.board[turn_choice[-2]][turn_choice[-1]].piece = piece
        else:
            pass
        print(self.board)


def main():
    G = Game('red')
    print(G.board)
    G.take_turn()


if __name__ == '__main__':
    main()
