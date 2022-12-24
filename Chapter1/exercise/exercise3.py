from typing import TypeVar, Generic, List
T = TypeVar('T')


class Stack(Generic[T]):

    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


def hanoi(begin: int, end: int, temp: int, n: int) -> None:
    if n == 1:
        towers[end].push(towers[begin].pop())
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)


total: int = 20
towers: List[Stack[int]] = []
for i in range(0, total):
    towers.append(Stack())
for i in range(0, total):
    towers[0].push(i)

print(len(towers))
if __name__ == "__main__":
    hanoi(0, len(towers) - 1, 1, total)
    for i in range(0, total):
        print(towers[i])
