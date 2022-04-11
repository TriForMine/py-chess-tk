from collections import defaultdict
from typing import Tuple, DefaultDict, Optional

from piece import Piece


def enemy_color(color: str):
    if color == "black":
        return "white"
    else:
        return "black"


def calculate_total_score(grid: DefaultDict[Tuple[int, int], Optional[Piece]]):
    total_score = 0
    for ((x, y), piece) in grid.items():
        if piece:
            if piece.color == "black":
                total_score -= piece.get_score(x, y)
            else:
                total_score += piece.get_score(x, y)

    return total_score
