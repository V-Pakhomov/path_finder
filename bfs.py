def bfs(field, current_squares, used_squares):
    square = current_squares.pop(0)
    for sq in square.neighbours(field):
        sq = field.nodes[sq]
        if sq not in current_squares and sq not in used_squares:
            current_squares.append(sq)
            sq.parent = square
            sq.path_to_start = square.path_to_start + sq.weight
            if sq != field.end:
                sq.light()
    used_squares.append(square)
    if square not in (field.start, field.end):
        square.dark()
