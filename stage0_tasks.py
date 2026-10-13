"""Этап 0 — диагностика по Python.

Реализуй функции и классы ниже так, чтобы прошли тесты из tests/test_stage0.py.
Запуск:  uv run pytest -v

Правила:
- только стандартная библиотека (без pandas и т. п.);
- везде, где можно, используй type hints;
- не подглядывай в тесты раньше, чем попробуешь сам по описанию.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T")
K = TypeVar("K")


# 1. Строки, словари, сортировка ------------------------------------------------
def word_freq(text: str, top: int) -> list[tuple[str, int]]:
    """Вернуть `top` самых частых слов в тексте.

    - Регистр не учитывается: "Кот" и "кот" — одно слово.
    - Словом считается последовательность букв и цифр; знаки препинания отбрасываются.
    - Сортировка: по убыванию частоты, при равенстве — по алфавиту.

    >>> word_freq("Кот, кот и пёс. Пёс!", 2)
    [('кот', 2), ('пёс', 2)]
    """
    raise NotImplementedError


# 2. Функции высшего порядка ----------------------------------------------------
def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Сгруппировать элементы по значению key(item), сохраняя исходный порядок.

    >>> group_by(["apple", "avocado", "banana"], key=lambda s: s[0])
    {'a': ['apple', 'avocado'], 'b': ['banana']}
    """
    raise NotImplementedError


# 3. Генераторы -----------------------------------------------------------------
def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Генератор: отдаёт элементы пачками по `size`, последняя пачка может быть короче.

    Должен работать с бесконечными итераторами (не превращай вход в список целиком).
    При size < 1 — ValueError.

    >>> list(chunked(range(5), 2))
    [[0, 1], [2, 3], [4]]
    """
    raise NotImplementedError


# 4. Декораторы -----------------------------------------------------------------
def retry(times: int, exceptions: tuple[type[BaseException], ...] = (Exception,)):
    """Декоратор: повторяет вызов функции до `times` раз, если она бросает
    одно из `exceptions`. Если все попытки неудачны — пробрасывает последнее исключение.
    Исключения других типов пробрасываются сразу, без повторов.
    Имя и докстринг обёрнутой функции должны сохраниться.

    @retry(times=3, exceptions=(ConnectionError,))
    def fetch(): ...
    """
    raise NotImplementedError


# 5. ООП, dataclasses, собственные исключения -----------------------------------
class InsufficientFundsError(Exception):
    """Недостаточно средств на счёте."""


class BankAccount:
    """Банковский счёт. Сделай его через @dataclass.

    Поля:
      owner: str
      balance: float = 0.0
      history: list[tuple[str, float]] — по умолчанию пустой список
                (осторожно с изменяемыми значениями по умолчанию!)

    Методы:
      deposit(amount)  — amount <= 0 → ValueError; пишет в history ("deposit", amount)
      withdraw(amount) — amount <= 0 → ValueError;
                         amount > balance → InsufficientFundsError;
                         пишет в history ("withdraw", amount)
    """


# 6. Контекстные менеджеры ------------------------------------------------------
class Timer:
    """Контекстный менеджер, измеряющий время выполнения блока.

    with Timer() as t:
        do_work()
    print(t.elapsed)  # секунды, float

    Используй time.perf_counter. Исключения внутри блока не подавлять.
    """


# 7. Файлы и модуль csv ---------------------------------------------------------
def csv_column_means(path: str) -> dict[str, float]:
    """Прочитать CSV с заголовком и вернуть среднее для каждого числового столбца.

    - Столбец считается числовым, если ВСЕ его непустые значения парсятся как float.
    - Пустые ячейки пропускаются.
    - Нечисловые столбцы в результат не попадают.
    - Столбец, где все ячейки пустые, в результат не попадает.
    """
    raise NotImplementedError