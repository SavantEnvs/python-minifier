def f(x, y=2):
    """doc"""
    assert x > 0
    return x + y


class C:
    value: int = 0

    async def go(self):
        async with open("f") as fh:
            return [i for i in range(10) if i % 2 == 0]


if __name__ == "__main__":
    import math
    print(f(math.pi), f"{C.value!r:>10}")
