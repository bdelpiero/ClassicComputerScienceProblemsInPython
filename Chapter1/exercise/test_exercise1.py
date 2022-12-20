from exercise1 import fib5, fib_golden


def test_fibonacci():
    # Test the first few Fibonacci numbers
    assert fib5(0) == fib_golden(0)
    assert fib5(2) == fib_golden(2)
    assert fib5(3) == fib_golden(3)
    assert fib5(1) == fib_golden(1)
    assert fib5(4) == fib_golden(4)
    assert fib5(5) == fib_golden(5)

    # Test a few arbitrary numbers
    assert fib5(10) == fib_golden(10)
    assert fib5(15) == fib_golden(15)
    assert fib5(20) == fib_golden(20)
