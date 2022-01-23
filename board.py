import random

BOARD_WIDTH = 5
BOARD_HEIGHT = 5

ALLOW_START_SELECTING_WITH_NEXT_SELECTION = False


class Board:
    def __init__(self):
        # Columns don't interact between each other. Let's treat each column as a list
        # The first column is on the left, and the first element is at the bottom
        self.columns: list[list[int]] = []
        self.empty()
        # 0 means empty place, and values from ord('A') to ord('Z') means a tile

        self.current_chr_list: list[str] = []
        self.current_sequence: list[tuple[int, int]] = []
        self.is_selecting: bool = False


    @staticmethod
    def pure_random():
        return random.randint(ord('A'), ord('Z'))

    def empty(self):
        self.columns = [[0 for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]

    def fill_prepare(self):
        for column in self.columns:
            to_add = column.count(0)
            for _ in range(to_add):
                column.append(self.pure_random())

    def eliminate_empty(self):
        for column in self.columns:
            to_eliminate = column.count(0)
            for _ in range(to_eliminate):
                column.remove(0)

    def start_select(self, x: int, y: int) -> list[str]:
        if x < 0 or \
                y < 0 or \
                x >= BOARD_WIDTH or\
                y >= BOARD_WIDTH:
            raise IndexError
        assert not (self.current_chr_list or self.current_sequence)
        assert self.is_selecting is False

        self.current_chr_list.append(chr(self.columns[x][y]))
        self.current_sequence.append((x, y))
        self.is_selecting = True
        return self.current_chr_list

    def next_select(self, x: int, y: int) -> (bool, list[str]):
        if x < 0 or \
                y < 0 or \
                x >= BOARD_WIDTH or\
                y >= BOARD_WIDTH:
            raise IndexError
        assert len(self.current_chr_list) == len(self.current_sequence)
        assert self.current_chr_list and self.current_sequence

        if ALLOW_START_SELECTING_WITH_NEXT_SELECTION:
            if self.is_selecting is False:
                return True, self.start_select(x, y)
        else:
            assert self.is_selecting is True

        if len(self.current_sequence) >= 2 and \
                self.current_sequence[-2] == (x, y):
            # Falling back
            self.current_sequence.pop()
            self.current_chr_list.pop()
            return True, self.current_chr_list

        if (x, y) in self.current_sequence:
            # This is not a new tile
            return False, self.current_chr_list

        current = self.current_sequence[-1]
        if current == (x, y):
            # The tile is same as the current head
            return False, self.current_chr_list
        d_x = current[0] - x
        d_y = current[1] - y
        if d_x not in (-1, 0, 1) or \
                d_y not in (-1, 0, 1):
            # this is not a neighbor of the current head
            return False, self.current_chr_list

        self.current_chr_list.append(chr(self.columns[x][y]))
        self.current_sequence.append((x, y))
        return True, self.current_chr_list

    def end_select(self):
        assert len(self.current_chr_list) == len(self.current_sequence)
        assert self.current_chr_list and self.current_sequence
        assert self.is_selecting is True

        self.is_selecting = False
        return self.current_chr_list

    @staticmethod
    def get_board_rot(columns):
        board_rot = [  # inverse of the board here
            [columns[x][y] for x in range(BOARD_WIDTH)]
            for y in range(BOARD_HEIGHT)
        ]
        board_rot.reverse()
        return board_rot

    @staticmethod
    def get_board_repr(columns: list[list[int]], sequence: list[tuple[int, int]]):
        upper_to_lower = ord('a') - ord('A')
        columns_copy = [column.copy() for column in columns]
        for coord in sequence:
            columns_copy[coord[0]][coord[1]] += upper_to_lower
        rot_ = Board.get_board_rot(columns_copy)
        characterized_ = [list(map(chr, row)) for row in rot_]
        repr_list = [repr(row) for row in characterized_]
        repr_dirty = "\n".join(repr_list)
        repr_clean = repr_dirty.replace('\\x00', ' ')
        return repr_clean

    def __repr__(self):
        # The logic of repr is no more tied to `self`
        #  in order to reflect current sequence on the board
        # Might as well just make it a separate staticmethod
        return self.get_board_repr(self.columns, self.current_sequence)

    def get_board_columns_repr(self):
        characterized_ = [list(map(chr, column)) for column in self.columns]
        repr_list = [repr(column) for column in characterized_]
        repr_dirty = "\n".join(repr_list)
        repr_clean = repr_dirty.replace('\\x00', ' ')
        return repr_clean

    def selection_clear(self):
        assert self.is_selecting is False

        self.current_chr_list.clear()
        self.current_sequence.clear()

    def remove_selected_tiles(self):
        assert self.is_selecting is False

        for coord in self.current_sequence:
            self.columns[coord[0]][coord[1]] = 0

    def selection_eval(self):
        # NYI: search dictionary
        print("DUMMY: word is always correct")
        rtn = True

        if rtn:
            self.remove_selected_tiles()
        self.selection_clear()
        return rtn


def test_main():
    import readline
    import word_evaluation
    word_evaluation.Evaluation.load()
    board = Board()
    try:
        while True:
            board.fill_prepare()
            board.eliminate_empty()
            while True:
                print(board)
                print(f"current word = {board.current_chr_list}")
                cmd = input("move? ")
                cmd.strip()
                cmd_list = cmd.split()
                match cmd_list[0]:
                    case 'S':
                        board.start_select(int(cmd_list[1]), int(cmd_list[2]))
                    case 'N':
                        board.next_select(int(cmd_list[1]), int(cmd_list[2]))
                    case 'E':
                        word = "".join(board.end_select())
                        print(word)
                        eval_result = word_evaluation.Evaluation.eval(word)
                        print(eval_result)
                        if not eval_result:
                            board.selection_clear()
                            continue
                        board.remove_selected_tiles()
                        board.selection_clear()
                        break

    except KeyboardInterrupt:
        print()
        print("Cya!")


if __name__ == "__main__":
    test_main()
