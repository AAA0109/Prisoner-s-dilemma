from otree.api import *
import random
from pathlib import Path

doc = """
Multiplayer word search game
"""


def load_word_list():
    # words from https://github.com/dovenokan/oxford-words
    return set(Path(__name__ + '/words.txt').read_text().split())


class C(BaseConstants):
    NAME_IN_URL = 'wordsearch'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    DIM = 5
    NUM_SQUARES = DIM * DIM
    LEXICON = load_word_list()

    COORDS = []

    for x in range(DIM):
        for y in range(DIM):
            COORDS.append((x, y))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    board = models.LongStringField()


class Player(BasePlayer):
    score = models.IntegerField(initial=0)


class FoundWord(ExtraModel):
    word = models.StringField()
    player = models.Link(Player)
    group = models.Link(Group)


def word_in_board(word, board):
    lengths = list(range(1, len(word) + 1))
    paths = {_: [] for _ in lengths}

    for i in range(C.DIM):
        for j in range(C.DIM):
            coord = (i, j)
            if board[coord] == word[0]:
                paths[1].append([coord])

    for length in lengths[1:]:
        target_char = word[length - 1]
        for path in paths[length - 1]:
            cur_x, cur_y = path[-1]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    check_coord = (cur_x + dx, cur_y + dy)
                    if (
                        check_coord in C.COORDS
                        and board[check_coord] == target_char
                        and check_coord not in path
                    ):
                        paths[length].append(path + [check_coord])
    return bool(paths[len(word)])


def load_board(board_str):
    return dict(zip(C.COORDS, board_str.replace('\n', '').lower()))


class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        rows = []
        for _ in range(C.DIM):
            # add extra vowels
            row = ''.join(
                [random.choice('AAABCDEEEEEFGHIIKLMNNOOPRRSTTUUVWXYZ') for _ in range(C.DIM)]
            )
            rows.append(row)
        group.board = '\n'.join(rows)


def live_method(player: Player, data):
    group = player.group
    board = group.board

    if 'word' in data:
        word = data['word'].lower()
        is_in_board = len(word) >= 3 and word_in_board(word, load_board(board))
        is_in_lexicon = is_in_board and word.lower() in C.LEXICON
        is_valid = is_in_board and is_in_lexicon
        already_found = is_valid and bool(FoundWord.filter(group=group, word=word))
        success = is_valid and not already_found
        news = dict(
            word=word,
            success=success,
            is_in_board=is_in_board,
            is_in_lexicon=is_in_lexicon,
            already_found=already_found,
            id_in_group=player.id_in_group,
        )
        if success:
            FoundWord.create(group=group, word=word)
            player.score += 1
    else:
        news = {}
    scores = [[p.id_in_group, p.score] for p in group.get_players()]
    found_words = [fw.word for fw in FoundWord.filter(group=group)]
    return {0: dict(news=news, scores=scores, found_words=found_words)}


class Play(Page):
    live_method = live_method
    timeout_seconds = 3 * 60

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(board=group.board.upper().split('\n'))

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)


class Results(Page):
    pass


page_sequence = [WaitToStart, Play, Results]
