import random
from math import lcm

from backend import word_evaluation

BOARD_WIDTH = 5
BOARD_HEIGHT = 5

ALLOW_START_SELECTING_WITH_NEXT_SELECTION = False

# Letter scores from official scrabble rule
LETTER_SCORE = [
    1, 3, 3, 2, 1,  # A - E
    4, 2, 4, 1, 8,  # F - J
    5, 1, 3, 1, 1,  # K - O
    3, 10, 1, 1, 1,  # P - T
    1, 4, 4, 8, 4, 10  # U - Z
]
THE_LETTER_FREQ = [
    9, 2, 2, 4, 12,  # A - E
    2, 3, 2, 9, 1,  # F - J
    1, 4, 2, 6, 8,  # K - O
    2, 1, 6, 4, 6,  # P - T
    4, 2, 2, 1, 2, 1  # U - Z
]


class Tile:
    # Simple class to handle {double,triple} {letter,word} bonuses
    def __init__(self, letter_ord, bonus: None | str = None):
        # A tile cannot have bonus while being an empty one
        assert not (letter_ord == 0 and bonus is not None)

        self.letter_ord = letter_ord
        self.bonus = bonus

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.letter_ord == other.letter_ord and self.bonus == other.bonus


class Board:
    COLUMNS_TYPE = list[list[Tile]]

    def __init__(self):
        # Columns don't interact between each other. Let's treat each column as a list
        # The first column is on the left, and the first element is at the bottom
        self.columns: Board.COLUMNS_TYPE = []
        self.fall_distance: list[list[int]] = []
        self.empty()
        # 0 means empty place, and values from ord('A') to ord('Z') means a tile

        self.current_chr_seq: list[str] = []
        self.current_coord_seq: list[tuple[int, int]] = []
        self.is_selecting: bool = False
        self.deselect: [tuple[int, int] | None] = None

        # TODO: add seeded random
        self.random_ = Board.Random(random.SystemRandom().randbytes(16).hex())

        # TODO: add scoring
        # TODO: add double/triple letter/word bonus

    class Random:
        def __init__(self, seed):
            self.seed = seed
            self.random = random.Random(bytes.fromhex(self.seed))

            self.random_table = self.get_inverse_weighted_table()
            self.random_table_sum = sum(self.random_table)

        @staticmethod
        def get_pure_random_table():
            return [1 for _ in range(26)]

        @staticmethod
        def get_complementary_weighted_table():
            print("comp_random_init")
            table = []
            sum_ = max(LETTER_SCORE) + 1
            for i in LETTER_SCORE:
                table.append(sum_ - i)
            return table

        @staticmethod
        def get_inverse_weighted_table():
            print("inv_random_init")
            table = []
            lcm_ = lcm(*LETTER_SCORE)
            for i in LETTER_SCORE:
                assert lcm_ % i == 0
                table.append(lcm_ // i)
            return table

        @staticmethod
        def the_freq_table():
            return THE_LETTER_FREQ

        def get_random_ascii(self):
            rand = self.random.randint(0, self.random_table_sum - 1)
            for nth, score in enumerate(self.random_table):
                rand -= score
                if rand < 0:
                    return nth + ord('A')
            raise AssertionError("board random tried to return None")

    def empty(self):
        self.columns = [[Tile(0) for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
        self.fall_distance = [[] for _ in range(BOARD_WIDTH)]
        self.deselect = None

    def fill_prepare(self):
        for i, column in enumerate(self.columns):
            to_add = column.count(Tile(0))
            for _ in range(to_add):
                rand = Tile(self.random_.get_random_ascii())
                column.append(rand)

            self.fall_distance[i] = []
            temp_fall_distance = 0
            for e in column:
                if e == Tile(0):
                    temp_fall_distance += 1
                    self.fall_distance[i].append(-1)
                    continue
                self.fall_distance[i].append(temp_fall_distance)

    def eliminate_empty(self):
        for column in self.columns:
            to_eliminate = column.count(Tile(0))
            for _ in range(to_eliminate):
                column.remove(Tile(0))

    def start_select(self, x: int, y: int) -> list[str]:
        if x < 0 or \
                y < 0 or \
                x >= BOARD_WIDTH or\
                y >= BOARD_WIDTH:
            raise IndexError
        assert not (self.current_chr_seq or self.current_coord_seq)
        assert self.is_selecting is False

        self.current_chr_seq.append(chr(self.columns[x][y].letter_ord))
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

        self.current_chr_seq.append(chr(self.columns[x][y].letter_ord))
        self.current_coord_seq.append((x, y))
        return True, self.current_chr_seq

    def end_select(self):
        assert len(self.current_chr_seq) == len(self.current_coord_seq)
        assert self.current_chr_seq and self.current_coord_seq
        assert self.is_selecting is True

        self.is_selecting = False
        return self.current_chr_seq

    @staticmethod
    def get_board_repr(columns: COLUMNS_TYPE, sequence: list[tuple[int, int]]):
        def get_board_rot_ord(columns_: Board.COLUMNS_TYPE) -> list[list[int]]:
            board_rot = [  # inverse of the board here
                [columns_[x][y].letter_ord for x in range(BOARD_WIDTH)]
                for y in range(BOARD_HEIGHT)
            ]
            board_rot.reverse()
            return board_rot
        columns_copy = [column.copy() for column in columns]
        for coord in sequence:  # upper to lower
            columns_copy[coord[0]][coord[1]] += ord('a') - ord('A')
        rot_ = get_board_rot_ord(columns_copy)
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

    def eval_after_select(self):
        assert self.is_selecting is False
        assert self.current_chr_seq
        assert self.current_coord_seq

        score = self.eval_score()

        if self.eval_word():
            # remove_selection_seq_from_board
            for i, coord in enumerate(self.current_coord_seq):
                assert self.columns[coord[0]][coord[1]].letter_ord == ord(self.current_chr_seq[i])
                self.columns[coord[0]][coord[1]] = Tile(0)
        else:
            score = -score

        # selection_seq_clear
        self.current_chr_seq.clear()
        self.current_coord_seq.clear()
        return score

    def eval_score(self):
        assert self.current_chr_seq
        assert self.current_coord_seq

        score = 0
        for i in self.current_chr_seq:
            score += LETTER_SCORE[ord(i) - ord('A')]
        return score

    def eval_word(self):
        # Evaluation can reject shorter words by not loading them, but Qu can mess this up
        if len(self.current_chr_seq) < 3:
            return False

        return word_evaluation.Evaluation.eval(
            self.get_current_word()
        )

    def get_current_word(self):
        seq_eval = self.current_chr_seq.copy()
        while 'Q' in seq_eval:
            seq_eval[seq_eval.index('Q')] = 'QU'
        return "".join(seq_eval)

    # TODO: Add undo / redo
    #  Restore random state on undo
    #  Burn entropy after a move, in order to not give the same new tile after different move


def test_main():
    import readline
    board = Board()
    try:
        while True:
            board.fill_prepare()
            board.eliminate_empty()
            while True:
                print(board)
                if board.is_selecting:
                    print(f"current word = {board.get_current_word()}, score = {board.eval_score()}")
                cmd = input("move? ")
                cmd.strip()
                cmd_list = cmd.split()
                match cmd_list[0]:
                    case 'S':
                        board.start_select(int(cmd_list[1]), int(cmd_list[2]))
                    case 'N':
                        board.next_select(int(cmd_list[1]), int(cmd_list[2]))
                    case 'E':
                        board.end_select()
                        print(board.get_current_word())
                        break
            ret = board.eval_after_select()
            print(f"{abs(ret)} {'won' if (ret > 0) else 'discarded'}")

    except KeyboardInterrupt:
        print()
        print("Cya!")


if __name__ == "__main__":
    test_main()
