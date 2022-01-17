class Piece:
    def __init__(
        self,
        color: str,
        king: bool = False
    ):
        assert isinstance(color, str)
        assert color.lower() in ['black', 'red']
        self._color = color.lower()
        self.king = king

    def __repr__(self):
        return f"Piece({self._color}, {self.king})"

    def __str__(self):
        printable = ""
        if self.king:
            printable += "K-"
        if self._color == 'red':
            printable += 'RED'
        else:
            printable += 'BLA'
        return printable


class Cell:
    def __init__(
        self,
        name: str,
        habitable: bool = False,
        piece: Piece = None
    ):
        self._name = name
        self.habitable = habitable
        self.piece = piece

    def __repr__(self):
        return f"Cell({self._name}, {self.habitable}, {self.piece})"

    def __str__(self):
        printable = f"Cell {self._name}"
        if self.habitable:
            printable += " is habitable"
            if self.piece is not None:
                printable += f" containing {self.piece}"
        else:
            printable += " is not habitable"
        return printable + "."


class Board:
    def __init__(self):
        self._rows = list('ABCDEFGH')
        self._columns = list(range(8))
        self.board = [
            [
                Cell(
                    name=f"{row}{col}",
                    habitable=self._is_habitable(
                        self._rows.index(row),
                        self._columns.index(col)),
                    piece=self._starting_piece(
                        self._rows.index(row),
                        self._columns.index(col)))
                for col in self._columns
            ] for row in self._rows
        ]

    @staticmethod
    def _is_habitable(row_index, col_index):
        return bool((row_index + col_index) % 2)

    def _starting_piece(self, row_index, col_index):
        if row_index <= 2 and self._is_habitable(row_index, col_index):
            return Piece('red', False)
        elif row_index >= 5 and self._is_habitable(row_index, col_index):
            return Piece('black', False)
        else:
            return None

    def __str__(self):
        h_separator = "+".join(["-" * 5 for _ in range(8)])
        rep_lines = []
        for row in range(8):
            rep_lines.append(h_separator)
            rep_lines.append(
                "|".join([
                    c._name.ljust(4, ' ') + ("*" if c.habitable else " ")
                    for c in self.board[row]
                ]))
            rep_lines.append(
                "|".join([
                    str(c.piece).ljust(5, ' ') if c.piece is not None else " " * 5
                    for c in self.board[row]
                ]))
        rep_lines.append(h_separator)
        return "\n".join(rep_lines)

    def __repr__(self):
        return self.__str__()
