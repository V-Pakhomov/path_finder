def main_algorithm(field, current_squares, used_squares, best_square, condition):
    current_squares.remove(best_square)
    for sq in best_square.neighbours(field):
        sq = field.nodes[sq]
        if condition(sq):
            current_squares.append(sq)
            sq.parent = best_square
            sq.path_to_start = best_square.path_to_start + sq.cost
            if sq != field.end:
                sq.light()
    used_squares.append(best_square)
    if best_square not in (field.start, field.end):
        best_square.dark()


def bfs(field, current_squares, used_squares):
    best_square = current_squares[0]
    condition = lambda sq: sq not in current_squares and sq not in used_squares
    main_algorithm(field, current_squares, used_squares, best_square, condition)


def greedy(field, current_squares, used_squares):
    best_square = min(current_squares, key=lambda sq: sq.dist_to_end)
    condition = lambda sq: sq not in current_squares and sq not in used_squares
    main_algorithm(field, current_squares, used_squares, best_square, condition)


def dijkstra(field, current_squares, used_squares):
    best_square = min(current_squares, key=lambda sq: sq.path_to_start)
    condition = lambda sq: sq not in used_squares and sq.path_to_start > best_square.path_to_start + sq.cost
    main_algorithm(field, current_squares, used_squares, best_square, condition)


def A_star(field, current_squares, used_squares):
    best_square = min(current_squares, key=lambda sq: sq.path_to_start + sq.dist_to_end)
    condition = lambda sq: (sq not in used_squares and
                            sq.path_to_start > best_square.path_to_start + sq.cost)
    main_algorithm(field, current_squares, used_squares, best_square, condition)
