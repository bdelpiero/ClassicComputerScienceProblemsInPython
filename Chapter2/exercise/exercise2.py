# Need to fix imports
# to test it, i copied the files to this dir,
# but should be able to import from parent dir

from maze import Maze, MazeLocation, manhattan_distance
from generic_search import dfs, bfs, astar
from typing import Callable, TypeVar

T = TypeVar('T')

if __name__ == "__main__":
    dfs_total: int = 0
    bfs_total: int = 0
    astar_total: int = 0

    for _ in range(0, 100):
        m: Maze = Maze()

        _, count = dfs(m.start, m.goal_test, m.successors)
        dfs_total += count

        _, count = bfs(m.start, m.goal_test, m.successors)
        bfs_total += count

        distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
        _, count = astar(m.start, m.goal_test, m.successors, distance)
        astar_total += count

    print("dfs went through an avg of {}.\n"
          .format(dfs_total/100))
    print("bfs went through an avg of {}.\n"
          .format(bfs_total/100))
    print("astar went through an avg of {}.\n"
          .format(astar_total/100))
