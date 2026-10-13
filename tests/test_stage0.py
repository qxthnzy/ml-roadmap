import itertools
import time

import pytest

from stage0_tasks import (
    BankAccount,
    InsufficientFundsError,
    Timer,
    chunked,
    csv_column_means,
    group_by,
    retry,
    word_freq,
)


# 1. word_freq ------------------------------------------------------------------
def test_word_freq_basic():
    assert word_freq("Кот, кот и пёс. Пёс!", 2) == [("кот", 2), ("пёс", 2)]


def test_word_freq_ties_sorted_alphabetically():
    assert word_freq("b a c a b c d", 3) == [("a", 2), ("b", 2), ("c", 2)]


def test_word_freq_top_larger_than_vocab():
    assert word_freq("one two", 10) == [("one", 1), ("two", 1)]


def test_word_freq_empty():
    assert word_freq("", 3) == []
    assert word_freq("!!! ...", 3) == []


# 2. group_by -------------------------------------------------------------------
def test_group_by_keeps_order():
    result = group_by(["apple", "avocado", "banana", "apricot"], key=lambda s: s[0])
    assert result == {"a": ["apple", "avocado", "apricot"], "b": ["banana"]}
    assert list(result) == ["a", "b"]


def test_group_by_numbers():
    assert group_by(range(6), key=lambda n: n % 2) == {0: [0, 2, 4], 1: [1, 3, 5]}


def test_group_by_empty():
    assert group_by([], key=len) == {}


# 3. chunked --------------------------------------------------------------------
def test_chunked_basic():
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_chunked_exact():
    assert list(chunked("abcd", 2)) == [["a", "b"], ["c", "d"]]


def test_chunked_is_lazy_on_infinite_iterator():
    gen = chunked(itertools.count(), 3)
    assert next(gen) == [0, 1, 2]
    assert next(gen) == [3, 4, 5]


def test_chunked_invalid_size():
    with pytest.raises(ValueError):
        list(chunked([1, 2], 0))


# 4. retry ----------------------------------------------------------------------
def test_retry_succeeds_after_failures():
    calls = {"n": 0}

    @retry(times=3, exceptions=(ConnectionError,))
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_retry_gives_up():
    calls = {"n": 0}

    @retry(times=2, exceptions=(ConnectionError,))
    def always_fails():
        calls["n"] += 1
        raise ConnectionError("still boom")

    with pytest.raises(ConnectionError, match="still boom"):
        always_fails()
    assert calls["n"] == 2


def test_retry_does_not_catch_other_exceptions():
    calls = {"n": 0}

    @retry(times=5, exceptions=(ConnectionError,))
    def bad():
        calls["n"] += 1
        raise KeyError("nope")

    with pytest.raises(KeyError):
        bad()
    assert calls["n"] == 1


def test_retry_passes_arguments_and_keeps_metadata():
    @retry(times=2)
    def add(a, b=0):
        """Складывает числа."""
        return a + b

    assert add(2, b=3) == 5
    assert add.__name__ == "add"
    assert add.__doc__ == "Складывает числа."


# 5. BankAccount ----------------------------------------------------------------
def test_account_flow():
    acc = BankAccount("Анна")
    acc.deposit(100)
    acc.withdraw(30)
    assert acc.balance == 70
    assert acc.history == [("deposit", 100), ("withdraw", 30)]


def test_account_errors():
    acc = BankAccount("Борис", balance=10)
    with pytest.raises(ValueError):
        acc.deposit(0)
    with pytest.raises(ValueError):
        acc.withdraw(-5)
    with pytest.raises(InsufficientFundsError):
        acc.withdraw(11)
    assert acc.balance == 10
    assert acc.history == []


def test_account_histories_are_independent():
    a, b = BankAccount("a"), BankAccount("b")
    a.deposit(1)
    assert b.history == []


def test_account_is_dataclass():
    import dataclasses

    assert dataclasses.is_dataclass(BankAccount)
    assert BankAccount("x", 5) == BankAccount("x", 5)


# 6. Timer ----------------------------------------------------------------------
def test_timer_measures():
    with Timer() as t:
        time.sleep(0.05)
    assert 0.04 <= t.elapsed < 1


def test_timer_does_not_swallow_exceptions():
    with pytest.raises(ZeroDivisionError):
        with Timer() as t:
            1 / 0
    assert t.elapsed >= 0


# 7. csv_column_means -----------------------------------------------------------
def test_csv_column_means(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text(
        "name,age,score,city,empty\n"
        "Анна,30,4.5,Москва,\n"
        "Борис,,3.5,Казань,\n"
        "Вера,20,abc,Пермь,\n",
        encoding="utf-8",
    )
    assert csv_column_means(str(path)) == {"age": 25.0}


def test_csv_column_means_all_numeric(tmp_path):
    path = tmp_path / "nums.csv"
    path.write_text("x,y\n1,10\n2,20\n3,30\n", encoding="utf-8")
    assert csv_column_means(str(path)) == {"x": 2.0, "y": 20.0}