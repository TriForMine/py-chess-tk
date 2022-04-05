from piece import Piece


def enemy_color(color: str):
    if color == "black":
        return "white"
    else:
        return "black"


def calculate_total_score(grid: list[list[Piece | None]]):
    total_score = 0
    for y in range(len(grid)):
        for piece in grid[y]:
            if piece:
                if piece.color == "black":
                    total_score -= piece.score
                else:
                    total_score += piece.score
    return total_score
