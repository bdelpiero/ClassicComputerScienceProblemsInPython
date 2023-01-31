from calendar import c
from math import floor
from tkinter import N
from typing import NamedTuple, List, Dict, Optional
from typing import TypeVar, Dict, List, Optional
from csp import CSP, Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


Grid = List[List[int]]  # type alias for grids


class GridLocation(NamedTuple):
    row: int
    column: int


# the empty spaces will be 0s
# TODO: assign randomly generated starting numbers or read sudoku from file
def generate_grid(rows: int, columns: int) -> Grid:
    return [[0 for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(str(row)))

# TODO: the domain for each variable shouldnt be 1-9. I should exclude the numbers already given by the starting grid
# In that way, I could start solving those numbers with fewer domains:
# https://levelup.gitconnected.com/csp-algorithm-vs-backtracking-sudoku-304a242f96d0


def generate_domain() -> List[int]:
    return [n for n in range(1, 10)]


def validate_rows(assignment: Dict[GridLocation, int]) -> bool:
    assigned_rows: Dict[int, List[int]] = {}
    for location, n in assignment.items():
        row = location.row
        if assigned_rows.get(row) == None:
            assigned_rows[row] = [n]
            continue

        if n in assigned_rows[row]:
            return True
        assigned_rows[row].append(n)
    return False


def validate_cols(assignment: Dict[GridLocation, int]) -> bool:
    assigned_columns: Dict[int, List[int]] = {}
    for location, n in assignment.items():
        column = location.column
        if assigned_columns.get(column) == None:
            assigned_columns[column] = [n]
            continue
        if n in assigned_columns[column]:
            return True
        assigned_columns[column].append(n)
    return False


def validate_boxes(assignment: Dict[GridLocation, int]) -> bool:
    boxes: Dict[GridLocation, List[int]] = {}
    for location, n in assignment.items():
        box_start_row = floor(location.row / 3)
        box_start_col = floor(location.column / 3)
        sub_grid: GridLocation = GridLocation(
            box_start_row, box_start_col)

        if boxes.get(sub_grid) == None:
            boxes[sub_grid] = [n]
            continue
        if n in boxes[sub_grid]:
            return True
        boxes[sub_grid].append(n)

    return False


class SudokuConstraint(Constraint[GridLocation, int]):
    def __init__(self, locations: List[GridLocation]) -> None:
        super().__init__(locations)
        self.locations: List[GridLocation] = locations

    def satisfied(self, assignment: Dict[GridLocation, int]) -> bool:
        return (not validate_rows(assignment) and
                (not validate_cols(assignment) and
                 (not validate_boxes(assignment))))


if __name__ == "__main__":
    sudoku_grid: Grid = [
        [7, 0, 0, 0, 0, 4, 8, 0, 0],
        [0, 0, 0, 0, 0, 5, 4, 0, 0],
        [0, 0, 9, 0, 0, 0, 7, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 9, 0],
        [8, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 1, 0, 0, 0, 0],
        [0, 3, 0, 0, 5, 0, 0, 0, 1],
        [0, 1, 0, 2, 0, 0, 0, 7, 5],
        [0, 0, 0, 1, 4, 3, 0, 0, 0]
    ]
    starting_assignments: Dict[GridLocation, int] = {}
    for i in range(len(sudoku_grid)):
        for j in range(len(sudoku_grid)):
            if sudoku_grid[i][j] == 0:
                continue
            starting_assignments[GridLocation(i, j)] = sudoku_grid[i][j]

    # TODO: improve
    possible_nums: Dict[GridLocation, List[int]] = {}
    locations: List[GridLocation] = []
    for i in range(len(sudoku_grid)):
        for j in range(len(sudoku_grid)):
            locations.append(GridLocation(i, j))
    for location in locations:
        possible_nums[location] = generate_domain()

    csp: CSP[GridLocation, int] = CSP(locations, possible_nums)
    csp.add_constraint(SudokuConstraint(locations))
    solution: Optional[Dict[GridLocation, int]
                       ] = csp.backtracking_search(starting_assignments)
    if solution is None:
        print("No solution found!")
    else:
        for grid_location, n in solution.items():
            sudoku_grid[grid_location.row][grid_location.column] = n

    display_grid(sudoku_grid)
