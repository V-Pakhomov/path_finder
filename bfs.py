from square import Square


def bfs(field, current_squares, used_squares):
    new_current_squares = []
    for square in current_squares:
        for sq in square.neighbours(field):
            sq = field.nodes[sq]
            if (sq not in new_current_squares and
                    sq not in current_squares and
                    sq not in used_squares):
                new_current_squares.append(sq)
                sq.parent = square
        used_squares.append(square)
        if square not in (field.start, field.end):
            square.dark()
    return new_current_squares
