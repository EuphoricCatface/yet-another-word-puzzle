import random
from math import lcm
from copy import deepcopy

from backend import word_evaluation

BOARD_WIDTH = 5
BOARD_HEIGHT = 5

ALLOW_START_SELECTING_WITH_NEXT_SELECTION = True
BOTTOM_ROW_IS_ALWAYS_BONUS = True
BOTTOM_ROW_BONUS_IS_ALWAYS_WORD = True
NEW_TILE_RANDOM_BONUS = True
NEW_TILE_BONUS_IS_ALWAYS_LETTER = True

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

    def __repr__(self):
        return f"{chr(self.letter_ord) if self.letter_ord else ' '}_{self.bonus if self.bonus else 'no'}"


COLUMNS_TYPE = list[list[Tile]]
COORD_SEQ_TYPE = list[tuple[int, int]]


class Board:
    def __init__(self):
        # Columns don't interact between each other. Let's treat each column as a list
        # The first column is on the left, and the first element is at the bottom
        self.columns: COLUMNS_TYPE = []
        self.fall_distance: list[list[int]] = []
        # 0 means empty place, and values from ord('A') to ord('Z') means a tile

        self.current_tile_seq: list[Tile] = []
        self.current_coord_seq: COORD_SEQ_TYPE = []
        self.is_selecting: bool = False
        self.deselect: [tuple[int, int] | None] = None

        # The following two are initialized in game_setup
        self.random: Board.Random | None = None
        self.move_history: Board.History | None = None

    def game_setup(self, seed=None):
        # TODO: add seeded random
        self.random = Board.Random(seed)
        self.move_history = Board.History(self.random.seed)
        self.empty()
        self.selection_seq_clear()
        self.is_selecting = False

    def empty(self):
        self.columns = [[Tile(0) for _ in range(BOARD_HEIGHT)] for _ in range(BOARD_WIDTH)]
        self.fall_distance = [[] for _ in range(BOARD_WIDTH)]
        self.deselect = None

    def selection_seq_clear(self):
        self.current_tile_seq.clear()
        self.current_coord_seq.clear()

    class Random:
        def __init__(self, seed):
            if seed is None:
                seed = random.SystemRandom().randbytes(16).hex()
            self.seed = seed
            self.random = random.Random(bytes.fromhex(self.seed))

            self.random_table = self.get_inverse_weighted_table()
            print(self.random_table)
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

        def get_random_bonus(self, dt_bitfield=3, lw_bitfield=3):
            bonus = None
            assert dt_bitfield-1 in range(3) and lw_bitfield-1 in range(3)
            pool = ["DL", "DW", "TL", "TW"]
            dt_bitfield = self.random.randint(0, 1) if dt_bitfield == 3 else dt_bitfield - 1
            lw_bitfield = self.random.randint(0, 1) if lw_bitfield == 3 else lw_bitfield - 1
            return pool[dt_bitfield * 2 + lw_bitfield]

        def get_new_tile(self, current_bonus_count=0):
            chr_ord = self.get_random_ascii()
            bonus = None
            # current_bonus_count is currently NYI in high level components
            if NEW_TILE_RANDOM_BONUS and current_bonus_count < 5:
                if self.random.randint(0, 49) < 4:
                    bonus = self.get_random_bonus(lw_bitfield=1 if NEW_TILE_BONUS_IS_ALWAYS_LETTER else 3)
            return Tile(chr_ord, bonus)

    def fill_prepare(self):
        for i, column in enumerate(self.columns):
            to_add = column.count(Tile(0))
            for _ in range(to_add):
                rand = self.random.get_new_tile()
                column.append(rand)

            self.fall_distance[i] = []
            temp_fall_distance = 0
            for e in column:
                if e == Tile(0):
                    temp_fall_distance += 1
                    self.fall_distance[i].append(-1)
                    continue
                self.fall_distance[i].append(temp_fall_distance)

            if BOTTOM_ROW_IS_ALWAYS_BONUS and column[0].letter_ord == 0:
                if self.random.random.randint(0, 10) == 0:
                    continue
                i = 0
                while column[i].letter_ord == 0:
                    i += 1
                lw_bitfield = 2 if BOTTOM_ROW_BONUS_IS_ALWAYS_WORD else 3
                column[i].bonus = self.random.get_random_bonus(lw_bitfield=lw_bitfield)

    def eliminate_empty(self):
        for column in self.columns:
            to_eliminate = column.count(Tile(0))
            for _ in range(to_eliminate):
                column.remove(Tile(0))

    def start_select(self, x: int, y: int) -> list[Tile]:
        if x < 0 or \
                y < 0 or \
                x >= BOARD_WIDTH or\
                y >= BOARD_WIDTH:
            raise IndexError
        assert not (self.current_tile_seq or self.current_coord_seq)
        assert self.is_selecting is False

        self.current_tile_seq.append(self.columns[x][y])
        self.current_coord_seq.append((x, y))
        self.is_selecting = True
        return self.current_tile_seq

    def next_select(self, x: int, y: int) -> (bool, list[str]):
        # TODO: allow farther candidates, selecting ones inbetween
        self.deselect = None
        if x < 0 or \
                y < 0 or \
                x >= BOARD_WIDTH or\
                y >= BOARD_WIDTH:
            raise IndexError
        assert len(self.current_tile_seq) == len(self.current_coord_seq)

        if ALLOW_START_SELECTING_WITH_NEXT_SELECTION:
            if self.is_selecting is False:
                return True, self.start_select(x, y)
        else:
            assert self.current_tile_seq and self.current_coord_seq
            assert self.is_selecting is True

        if len(self.current_coord_seq) >= 2 and \
                self.current_coord_seq[-2] == (x, y):
            # Falling back
            self.deselect = self.current_coord_seq.pop()
            self.current_tile_seq.pop()
            return True, self.current_tile_seq

        if (x, y) in self.current_coord_seq:
            # This is not a new tile
            return False, self.current_tile_seq

        current = self.current_coord_seq[-1]
        if current == (x, y):
            # The tile is same as the current head
            return False, self.current_tile_seq
        d_x = current[0] - x
        d_y = current[1] - y
        if d_x not in (-1, 0, 1) or \
                d_y not in (-1, 0, 1):
            # this is not a neighbor of the current head
            return False, self.current_tile_seq

        self.current_tile_seq.append(self.columns[x][y])
        self.current_coord_seq.append((x, y))
        return True, self.current_tile_seq

    def end_select(self):
        assert len(self.current_tile_seq) == len(self.current_coord_seq)
        assert self.current_tile_seq and self.current_coord_seq
        assert self.is_selecting is True

        self.is_selecting = False
        return self.current_tile_seq

    @staticmethod
    def get_board_repr(columns: COLUMNS_TYPE, sequence: list[tuple[int, int]]):
        def get_board_rot(columns_: COLUMNS_TYPE) -> COLUMNS_TYPE:
            board_rot = [  # inverse of the board here
                [columns_[x][y] for x in range(BOARD_WIDTH)]
                for y in range(BOARD_HEIGHT)
            ]
            board_rot.reverse()
            return board_rot

        columns_copy = [deepcopy(column) for column in columns]
        for coord in sequence:  # upper to lower - NOTE: DIRTY HACK!
            columns_copy[coord[0]][coord[1]].letter_ord += ord('a') - ord('A')
        rot_ = get_board_rot(columns_copy)
        repr_list = [repr(row) for row in rot_]
        repr_dirty = "\n".join(repr_list)
        repr_clean = repr_dirty.replace('\\x00', ' ')
        return repr_clean

    def __repr__(self):
        # The logic of repr is no more tied to `self`
        #  in order to reflect current sequence on the board
        # Might as well just make it a separate staticmethod
        return self.get_board_repr(self.columns, self.current_coord_seq)

    def eval_after_select(self, history=True):
        assert self.is_selecting is False
        assert self.current_tile_seq
        assert self.current_coord_seq

        score = self.eval_score()

        if self.eval_word():
            assert self.move_history
            if history:  # Skip these if undo/redo
                self.move_history.move_push(deepcopy(self.current_coord_seq), score)
                self.move_history.redo_purge()

            # remove_selection_seq_from_board
            for i, coord in enumerate(self.current_coord_seq):
                assert self.columns[coord[0]][coord[1]] == self.current_tile_seq[i]
                self.columns[coord[0]][coord[1]] = Tile(0)
        else:
            score = -score

        self.selection_seq_clear()
        return score

    def eval_score(self):
        assert self.current_tile_seq
        assert self.current_coord_seq

        score = 0
        word_modifier = 1
        for tile in self.current_tile_seq:
            letter_modifier = 1
            if tile.bonus == 'DL':
                letter_modifier = 2
            elif tile.bonus == 'TL':
                letter_modifier = 3
            elif word_modifier < 2 and tile.bonus == 'DW':
                word_modifier = 2
            elif word_modifier < 3 and tile.bonus == 'TW':
                word_modifier = 3
            score += LETTER_SCORE[tile.letter_ord - ord('A')] * letter_modifier
        return score * word_modifier

    def eval_word(self):
        # Evaluation can reject shorter words by not loading them, but Qu can mess this up
        if len(self.current_tile_seq) < 3:
            return False

        return word_evaluation.Evaluation.eval(
            self.get_current_word()
        )

    def get_current_word(self):
        chr_list = [chr(x.letter_ord) for x in self.current_tile_seq]
        while 'Q' in chr_list:
            chr_list[chr_list.index('Q')] = 'QU'
        return "".join(chr_list)

    class History:
        def __init__(self, seed):
            self.seed = seed
            self.moves: list[tuple[COORD_SEQ_TYPE, int]] = []
            self.redo_moves: list[COORD_SEQ_TYPE] = []

        def move_push(self, move: COORD_SEQ_TYPE, score: int):
            self.moves.append((move, score))

        def move_pop(self) -> (COORD_SEQ_TYPE, int):
            return self.moves.pop()

        def redo_push(self, move: COORD_SEQ_TYPE):
            self.redo_moves.append(move)

        def redo_pop(self) -> COORD_SEQ_TYPE:
            return self.redo_moves.pop()

        def redo_purge(self):
            self.redo_moves.clear()

        def has_undo(self):
            return bool(self.moves)

        def has_redo(self):
            return bool(self.redo_moves)

    def undo(self) -> (COORD_SEQ_TYPE, int):
        assert self.move_history.moves
        # Init the board with the seed, redo all the way to the move before.
        # Might be a bit slow, but implementation should be easier, right?

        # These will be returned so that GUI will know which tiles to move up, and how much to subtract from score
        last_move, last_score = self.move_history.move_pop()

        # Init board
        self.selection_seq_clear()
        self.is_selecting = False
        self.random = Board.Random(self.move_history.seed)
        self.empty()
        self.fill_prepare()
        self.eliminate_empty()

        # Perform move
        for move, _ in self.move_history.moves:
            for element in move:
                sel_rtn = self.next_select(*element)
                assert sel_rtn
            self.end_select()
            score = self.eval_after_select(history=False)
            assert score > 0
            self.fill_prepare()
            self.eliminate_empty()

        self.move_history.redo_push(last_move)
        return last_move, last_score

    def redo(self):
        assert self.move_history.redo_moves
        redo_move = self.move_history.redo_pop()

        # Perform move
        for element in redo_move:
            sel_rtn, _ = self.next_select(*element)
            assert sel_rtn
        self.end_select()
        score = self.eval_after_select(history=False)
        # `self.eval_after_select(history=True)` will purge `redo_moves`
        assert score > 0
        self.move_history.move_push(redo_move, score)

        self.fill_prepare()
        # Perform eliminate_empty separately afterwards. This is for GUI animation
        # self.eliminate_empty()
        return score


def test_main():
    import readline
    board = Board()
    board.game_setup()
    try:
        while True:
            end_turn = False
            board.fill_prepare()
            board.eliminate_empty()
            while True:
                print(board)
                if board.is_selecting:
                    print(f"current word = {board.get_current_word()}, score = {board.eval_score()}")
                print(f"{board.move_history.has_undo()=}, {board.move_history.has_redo()=}")
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
                        end_turn = True
                        break
                    case 'R':
                        board.redo()
                        board.eliminate_empty()
                    case 'U':
                        board.undo()
            if end_turn:
                ret = board.eval_after_select()
                print(f"{abs(ret)} {'won' if (ret > 0) else 'discarded'}")

    except KeyboardInterrupt:
        print()
        print("Cya!")


if __name__ == "__main__":
    test_main()
