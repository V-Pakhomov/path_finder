def greedy(field, current_squares, used_squares):
    closest_square = min(current_squares, key=lambda x: x.dist_to_end)
    current_squares.remove(closest_square)
    for sq in closest_square.neighbours(field):
        sq = field.nodes[sq]
        if sq not in current_squares and sq not in used_squares:
            current_squares.append(sq)
            sq.parent = closest_square
            sq.path_to_start = closest_square.path_to_start + sq.weight
            if sq != field.end:
                sq.light()
    used_squares.append(closest_square)
    if closest_square not in (field.start, field.end):
        closest_square.dark()
