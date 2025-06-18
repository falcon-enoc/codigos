from dataclasses import dataclass

@dataclass
class TestCase:
    nums: list
    target: int

# Crear objeto
test1 = TestCase([2, 7, 11, 15], 9)
test2 = TestCase([3, 2, 4], 6)
test3 = TestCase([3, 3], 6)
test4 = TestCase([1, 3, 4, 2], 6)


for test in [test1, test2, test3, test4]:
    for test.num in test.nums:
        if test.num + test.num == test.target:
            print(f"Output: {test.num}")
            break