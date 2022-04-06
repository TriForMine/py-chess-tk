from piece import Piece


def enemy_color(color: str):
    if color == "black":
        return "white"
    else:
        return "black"


def calculate_total_score(grid: list[list[Piece | None]]):
    total_score = 0
    for (y, line) in enumerate(grid):
        for (x, piece) in enumerate(line):
            if piece:
                if piece.color == "black":
                    total_score -= piece.get_score(x, y)
                else:
                    total_score += piece.get_score(x, y)

    return total_score
