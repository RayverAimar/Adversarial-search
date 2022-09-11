from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 5
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),  #Computer
    Player(label="O", color="green"), #Human
)