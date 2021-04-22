def A_star(field, current_squares, used_squares):
    best_dist_plus_path_square = min(current_squares, key=lambda x: x.path_to_start + x.dist_to_end)
    current_squares.remove(best_dist_plus_path_square)
    for sq in best_dist_plus_path_square.neighbours(field):
        sq = field.nodes[sq]
        if sq not in used_squares and sq.path_to_start > best_dist_plus_path_square.path_to_start + sq.weight:
            current_squares.append(sq)
            sq.parent = best_dist_plus_path_square
            sq.path_to_start = best_dist_plus_path_square.path_to_start + sq.weight
            if sq != field.end:
                sq.light()
    used_squares.append(best_dist_plus_path_square)
    if best_dist_plus_path_square not in (field.start, field.end):
        best_dist_plus_path_square.dark()
