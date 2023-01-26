
from turtle import width
from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase
from typing import TypeVar, Dict, List, Optional
from csp import CSP, Constraint

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type


Grid = List[List[str]]  # type alias for grids


class GridLocation(NamedTuple):
    row: int
    column: int


# the colors will be displayed as letter: R(red), B(blue), etc
# the empty spaces will be 0s
def generate_grid(rows: int, columns: int) -> Grid:
    return [['0' for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


class Chip(NamedTuple):
    color: str
    height: int
    width: int


def generate_subgrid(starting_row: int, starting_column: int, num_rows: int, num_columns: int) -> List[GridLocation]:
    subgrid = []
    for row in range(starting_row, starting_row + num_rows):
        for column in range(starting_column, starting_column + num_columns):
            subgrid.append(GridLocation(row, column))
    return subgrid


def generate_domain(chip_height: int, chip_width: int, recurse=True) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    grid_height: int = len(grid)
    grid_width: int = len(grid[0])

    for row in range(grid_height):
        for col in range(grid_width):
            if col + chip_width <= grid_width and row + chip_height <= grid_height:
                # could use list comprehension:  [ GridLocation(r, c) for r, c in product(rows, columns)]
                domain.append(generate_subgrid(
                    row, col, chip_height, chip_width))

    # rotate chip 90 degrees
    if recurse:
        return domain + generate_domain(chip.width, chip.height, False)

    return domain


class CircuitBoardConstraint(Constraint[Chip, List[GridLocation]]):
    def __init__(self, chips: List[Chip]) -> None:
        super().__init__(chips)
        self.chips: List[Chip] = chips

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # if there are any duplicates grid locations then there is an overlap
        all_locations = [locs for values in assignment.values()
                         for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    chips: List[Chip] = [Chip('b', 5, 1), Chip('g', 4, 4), Chip(
        'y', 3, 3), Chip('v', 2, 2), Chip('r', 2, 5)]
    locations: Dict[Chip, List[List[GridLocation]]] = {}
    for chip in chips:
        locations[chip] = generate_domain(chip.height, chip.width)

    csp: CSP[Chip, List[GridLocation]] = CSP(chips, locations)
    csp.add_constraint(CircuitBoardConstraint(chips))
    solution: Optional[Dict[Chip, List[GridLocation]]
                       ] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for chip, grid_locations in solution.items():
            for index in range(len(grid_locations)):
                (row, col) = (
                    grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = chip.color
        display_grid(grid)
