from typing import List, Iterable, Sequence, TypeVar, Protocol, Any
import time
import random

T = TypeVar('T')


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:  # while there is still a search space
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


def time_linear_search(ls: List[T], numsToFind: List[T]):
    start = time.time()
    for n in numsToFind:
        linear_contains(ls, n)
    end = time.time()
    return end - start


def time_binary_search(ls: Sequence[C], numsToFind: List[C]):
    start = time.time()
    for n in numsToFind:
        binary_contains(ls, n)
    end = time.time()
    return end - start


if __name__ == "__main__":
    nums = [x for x in range(1000000)]
    numsToFind = random.sample(range(0, 1000000), 1000)
    print("Linear search took {}.\n"
          .format(time_linear_search(nums, numsToFind)))
    print("Binary search took {}.\n"
          .format(time_binary_search(nums, numsToFind)))
