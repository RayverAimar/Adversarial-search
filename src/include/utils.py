from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str
    turn: bool

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue", turn=False),
    Player(label="O", color="green", turn=False),
)