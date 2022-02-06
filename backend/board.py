import random
from math import lcm

BOARD_WIDTH = 5
BOARD_HEIGHT = 5

ALLOW_START_SELECTING_WITH_NEXT_SELECTION = False

# Letter scores from official scrabble rule
LETTER_SCORE = [
    1, 3, 3, 2, 1,  # A - E
    4, 2, 4, 1, 8,  # F - J
    5, 1, 3, 1, 1,  # K - O
    3, 10, 1, 8, 1,  # P - T
    1, 4, 4, 8, 4, 10  # U - Z
]


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
        self.deselect: [tuple[int, int] | None] = None

        # TODO: add seeded random
        self.seed = random.SystemRandom().randbytes(16).hex()
        self.random = random.Random(bytes.fromhex(self.seed))

        # TODO: add scoring
        # TODO: add double/triple letter/word bonus

    def pure_random(self):
        return self.random.randint(ord('A'), ord('Z'))

    def complementary_weighted_random(self):
        if "reverse_score" not in Board.complementary_weighted_random.__dict__:
            print("random_init")
            Board.complementary_weighted_random.reverse_score = []
            sum_ = max(LETTER_SCORE) + 1
            for i in LETTER_SCORE:
                Board.complementary_weighted_random.reverse_score.append(sum_ - i)
            Board.complementary_weighted_random.sum = sum(Board.complementary_weighted_random.reverse_score)
        rand = self.random.randint(0, Board.complementary_weighted_random.sum)
        for nth, score in enumerate(Board.complementary_weighted_random.reverse_score):
            rand -= score
            if rand < 0:
                return nth + ord('A')

    def inverse_weighted_random(self):
        if "inverse_score" not in Board.inverse_weighted_random.__dict__:
            print("random_init")
            Board.inverse_weighted_random.inverse_score = []
            lcm_ = lcm(*LETTER_SCORE)
            for i in LETTER_SCORE:
                Board.inverse_weighted_random.inverse_score.append(lcm_ / i)
            Board.inverse_weighted_random.sum = sum(Board.inverse_weighted_random.inverse_score)
        rand = self.random.randint(0, Board.inverse_weighted_random.sum)
        for nth, score in enumerate(Board.inverse_weighted_random.inverse_score):
            rand -= score
            if rand < 0:
                return nth + ord('A')

    def empty(self):
        self.columns = [[0 for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
        self.fall_distance = [[] for _ in range(BOARD_WIDTH)]
        self.deselect = None

    def fill_prepare(self):
        for i, column in enumerate(self.columns):
            to_add = column.count(0)
            for _ in range(to_add):
                column.append(self.inverse_weighted_random())

            self.fall_distance[i] = []
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
        # TODO: allow farther candidates, selecting ones inbetween
        self.deselect = None
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
            self.deselect = self.current_coord_seq.pop()
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
