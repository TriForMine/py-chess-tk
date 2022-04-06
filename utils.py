from piece import Piece


def enemy_color(color: str):
    if color == "black":
        return "white"
    else:
        return "black"


def calculate_total_score(grid: list[list[Piece | None]]):
    total_score = 0
    for line in grid:
        for piece in line:
            if piece:
                if piece.color == "black":
                    total_score -= piece.score
                else:
                    total_score += piece.score
    return total_score
