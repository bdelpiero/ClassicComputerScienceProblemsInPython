import math

# calculates the nth number in the fibonacci sequence using the golden ratio


def fib_golden(n: int) -> int:
    golden_ratio = (1 + 5 ** 0.5) / 2
    return ((golden_ratio ** n) - (1 - golden_ratio) ** n) // math.sqrt(5)


# i declared this function here as a workaround
# couldn't import it directly to the test file from the parent dir


def fib5(n: int) -> int:
    if n == 0:
        return n  # special case
    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
    return next
