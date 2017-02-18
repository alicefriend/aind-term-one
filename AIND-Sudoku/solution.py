def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [r + c for r in A for c in B]


rows = "ABCDEFGHI"
cols = "123456789"

boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
col_units = [cross(rows, col) for col in cols]
square_units = [cross(rs, cs) for rs in ["ABC", "DEF", "GHI"] for cs in ["123", "456", "789"]]
peer_units = row_units + col_units + square_units
units = dict((s, [u for u in peer_units if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

left_diagonal = [row + col for i, row in enumerate(rows) for j, col in enumerate(cols) if i == j]
right_diagonal = [row + col for i, row in enumerate(rows) for j, col in enumerate(cols[::-1]) if i == j]
unitlist = row_units + col_units + square_units + [left_diagonal] + [right_diagonal]

assignments = []


def assign_value(values, box, value):
    """
    Use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        twins = [(box_1, box_2) for i, box_1 in enumerate(unit) for j, box_2 in enumerate(unit)
                 if i < j and values[box_1] == values[box_2] and len(values[box_1]) == 2]
        for twin in twins:
            box_1, box_2 = twin
            unit_except_twin = set(unit) - {box_1} - {box_2}
            for box in unit_except_twin:
                # if unsolvable, stop eliminating and return
                if len([box for box in values.keys() if values[box] == '']): return values

                assign_value(values, box, values[box].replace(values[box_1][0], ''))
                assign_value(values, box, values[box].replace(values[box_1][1], ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return {boxes[i] : "123456789" if value == "." else value for i, value in enumerate(grid)}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values == False:
        print("Failed! Unsolvable sudoku")
        return
        
    longest_length = max([len(values[box]) for box in values.keys()])
    form_each = "| {:^" + str(longest_length) + "} "
    form = form_each * 9 + "|"

    print("\n")
    for row in row_units:
        print(form.format(*[values[box] for box in row]))
    print("\n")


def eliminate(values):
    # Eliminate possible values that is in the same row, column and 3 by 3 square unit.
    fixed_boxes = [box for box in values if len(values[box]) == 1]
    for fixed_box in fixed_boxes:
        for box in peers[fixed_box]:
            assign_value(values, box, values[box].replace(values[fixed_box], ''))

    # Eliminate possible values that is in the same left diagonal or right diagonal.
    l_diag_fixed = [box for box in fixed_boxes if box in left_diagonal]
    r_diag_fixed = [box for box in fixed_boxes if box in right_diagonal]

    for fixed_box in l_diag_fixed:
        for box in set(left_diagonal) - {fixed_box}:
            assign_value(values, box, values[box].replace(values[fixed_box], ''))
    for fixed_box in r_diag_fixed:
        for box in set(right_diagonal) - {fixed_box}:
            assign_value(values, box, values[box].replace(values[fixed_box], ''))

    return values


def only_choice(values):
    """
    Select domain variable when it's impossible for all other box in the same unit to take the domain
    """
    for unit in unitlist:
        for digit in "123456789":
            candiate = [box for box in unit if digit in values[box]]
            if len(candiate) is 1:
                assign_value(values, candiate[0], digit)
    return values


def reduce_puzzle(values):
    """
    Keep reducing until no improvement can't be made without explicitly selecting domain
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        eliminate(values)
        only_choice(values)
        naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]): return False
    return values


def search(values):
    """
    Search solution using DFS search and Contraint propagtion
    """
    if reduce_puzzle(values) == False: return False

    domain_counts = {box: len(values[box]) for box in values.keys() if len(values[box]) >= 2}

    if domain_counts == {}: return values

    preferred_box = min(domain_counts, key=domain_counts.get)

    for choice in values[preferred_box]:
        values_copy = values.copy()
        values_copy[preferred_box] = choice
        result = search(values_copy)
        if result: return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
