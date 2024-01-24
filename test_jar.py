from jar import Jar
from pytest import raises


def test_init():
    jar = Jar()
    assert jar.capacity == 12

    jar = Jar(2)
    assert jar.capacity == 2
    assert jar.size == 0


def test_str():
    jar = Jar(15)
    assert str(jar) == ""

    jar.deposit(1)
    assert str(jar) == "🍪"

    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar(10)

    jar.deposit(2)
    assert jar.size == 2

    jar.deposit(1)
    assert jar.size == 3


def test_withdraw():
    jar = Jar(10)

    with raises(ValueError):
        jar.withdraw(2)

    jar.deposit(3)
    jar.withdraw(2)
    assert jar.size == 1