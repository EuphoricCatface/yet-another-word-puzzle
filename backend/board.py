import random

BOARD_WIDTH = 5
BOARD_HEIGHT = 5

ALLOW_START_SELECTING_WITH_NEXT_SELECTION = False


class Board:
    def __init__(self):
        # Columns don't interact between each other. Let's treat each column as a list
        # The first column is on the left, and the first element is at the bottom
        self.columns: list[list[int]] = []
        self.fall_distance: list[list[int]] = []
        self.empty()
        # 0 means empty place, and values from ord('A') to ord('Z') means a tile

        self.current_chr_seq: list[str] = []
        self.current_coord_seq: list[tuple[int, int]] = []
        self.is_selecting: bool = False

        # TODO: add seeded random
        self.seed = random.SystemRandom().randbytes(16).hex()
        self.random = random.Random(bytes.fromhex(self.seed))

    def pure_random(self):
        # TODO: add weighted random
        return self.random.randint(ord('A'), ord('Z'))

    def empty(self):
        self.columns = [[0 for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
        self.fall_distance = [[] for _ in range(BOARD_WIDTH)]

    def fill_prepare(self):
        for i, column in enumerate(self.columns):
            to_add = column.count(0)
            for _ in range(to_add):
                column.append(self.pure_random())

            temp_fall_distance = 0
            for e in column:
                if e == 0:
                    temp_fall_distance += 1
                    self.fall_distance[i].append(-1)
                    continue
                self.fall_distance[i].append(temp_fall_distance)

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
        assert not (self.current_chr_seq or self.current_coord_seq)
        assert self.is_selecting is False

        self.current_chr_seq.append(chr(self.columns[x][y]))
        self.current_coord_seq.append((x, y))
        self.is_selecting = True
        return self.current_chr_seq

    def next_select(self, x: int, y: int) -> (bool, list[str]):
        if x < 0 or \
                y < 0 or \
                x >= BOARD_WIDTH or\
                y >= BOARD_WIDTH:
            raise IndexError
        assert len(self.current_chr_seq) == len(self.current_coord_seq)
        assert self.current_chr_seq and self.current_coord_seq

        if ALLOW_START_SELECTING_WITH_NEXT_SELECTION:
            if self.is_selecting is False:
                return True, self.start_select(x, y)
        else:
            assert self.is_selecting is True

        if len(self.current_coord_seq) >= 2 and \
                self.current_coord_seq[-2] == (x, y):
            # Falling back
            self.current_coord_seq.pop()
            self.current_chr_seq.pop()
            return True, self.current_chr_seq

        if (x, y) in self.current_coord_seq:
            # This is not a new tile
            return False, self.current_chr_seq

        current = self.current_coord_seq[-1]
        if current == (x, y):
            # The tile is same as the current head
            return False, self.current_chr_seq
        d_x = current[0] - x
        d_y = current[1] - y
        if d_x not in (-1, 0, 1) or \
                d_y not in (-1, 0, 1):
            # this is not a neighbor of the current head
            return False, self.current_chr_seq

        self.current_chr_seq.append(chr(self.columns[x][y]))
        self.current_coord_seq.append((x, y))
        return True, self.current_chr_seq

    def end_select(self):
        assert len(self.current_chr_seq) == len(self.current_coord_seq)
        assert self.current_chr_seq and self.current_coord_seq
        assert self.is_selecting is True

        self.is_selecting = False
        return self.current_chr_seq

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
        return self.get_board_repr(self.columns, self.current_coord_seq)

    def get_board_columns_repr(self):
        characterized_ = [list(map(chr, column)) for column in self.columns]
        repr_list = [repr(column) for column in characterized_]
        repr_dirty = "\n".join(repr_list)
        repr_clean = repr_dirty.replace('\\x00', ' ')
        return repr_clean

    def selection_clear(self):
        assert self.is_selecting is False

        self.current_chr_seq.clear()
        self.current_coord_seq.clear()

    def remove_selected_tiles(self):
        assert self.is_selecting is False

        for coord in self.current_coord_seq:
            self.columns[coord[0]][coord[1]] = 0

    def selection_eval(self):
        # NYI: search dictionary
        print("DUMMY: word is always correct")
        rtn = True

        if rtn:
            self.remove_selected_tiles()
        self.selection_clear()
        return rtn

    # TODO: Add undo / redo
    #  Restore random state on undo
    #  Burn entropy after a move, in order to not give the same new tile after different move


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
                print(f"current word = {board.current_chr_seq}")
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
