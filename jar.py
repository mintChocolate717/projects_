class Jar:
    # initializes a cookie jar with the given capacity(the maximum number of cookies that can fit in the cookie jar)
    def __init__(self, capacity: int =12):
        self.capacity = capacity
        self.size = 0  # size is initially zero

    # GETTER for capacity
    @property
    def capacity(self):
        return self._capacity

    # SETTER for capacity:
    @capacity.setter
    def capacity(self, capacity: int):
        if capacity >= 0 and isinstance(
            capacity, int
        ):  # capacity must be a non-negative integer
            self._capacity = capacity
        else:  # If not, raise a ValueError.
            raise ValueError

    # GETTER for size
    @property
    def size(self):
        return (
            self._size
        )  # returns the number of cookies actually in the cookie jar, initially 0.

    # SETTER for size
    @size.setter
    def size(self, size: int = 0):
        self._size = size

    # adds n cookies to the cookie jar.
    def deposit(self, n: int):
        # If adding n cookies exceed the cookie jar’s capacity, raise a ValueError.
        if (self.size + n) > self.capacity:
            raise ValueError
        else:
            self.size += n

    # removes n cookies from the cookie jar. Nom nom nom.
    def withdraw(self, n: int):
        # If there aren’t n cookies in the cookie jar, raise a ValueError.
        if self.size < n:
            raise ValueError
        else:
            self.size -= n

    # returns a str with n 🍪, where n is the number of cookies in the cookie jar.
    def __str__(self) -> str:
        return "🍪" * self.size
