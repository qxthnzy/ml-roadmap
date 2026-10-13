from week2_tasks import (
    average,
    char_count,
    count_vowels,
    fizzbuzz,
    grade,
    is_even,
    is_palindrome,
    max_of_three,
    only_positive,
    sum_to,
)


# 1. is_even
def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False
    assert is_even(0) is True
    assert is_even(-2) is True


# 2. max_of_three
def test_max_of_three():
    assert max_of_three(3, 9, 5) == 9
    assert max_of_three(10, 2, 7) == 10
    assert max_of_three(1, 2, 3) == 3
    assert max_of_three(4, 4, 1) == 4
    assert max_of_three(-5, -2, -9) == -2


# 3. grade
def test_grade():
    assert grade(100) == "A"
    assert grade(90) == "A"
    assert grade(89) == "B"
    assert grade(75) == "B"
    assert grade(74) == "C"
    assert grade(60) == "C"
    assert grade(59) == "F"
    assert grade(0) == "F"


# 4. sum_to
def test_sum_to():
    assert sum_to(4) == 10
    assert sum_to(1) == 1
    assert sum_to(100) == 5050
    assert sum_to(0) == 0
    assert sum_to(-3) == 0


# 5. fizzbuzz
def test_fizzbuzz():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[-1] == "FizzBuzz"
    assert fizzbuzz(0) == []


# 6. count_vowels
def test_count_vowels():
    assert count_vowels("Hello World") == 3
    assert count_vowels("AEIOU") == 5
    assert count_vowels("rhythm") == 0
    assert count_vowels("") == 0


# 7. is_palindrome
def test_is_palindrome():
    assert is_palindrome("А роза упала на лапу Азора") is True
    assert is_palindrome("level") is True
    assert is_palindrome("python") is False
    assert is_palindrome("") is True


# 8. only_positive
def test_only_positive():
    assert only_positive([3, -1, 0, 5, -7]) == [3, 5]
    assert only_positive([-1, -2]) == []
    assert only_positive([]) == []


def test_only_positive_does_not_change_input():
    data = [1, -1]
    only_positive(data)
    assert data == [1, -1]


# 9. average
def test_average():
    assert average([2, 4, 6]) == 4.0
    assert average([5]) == 5.0
    assert average([1, 2]) == 1.5
    assert average([]) == 0.0


# 10. char_count
def test_char_count():
    assert char_count("мама") == {"м": 2, "а": 2}
    assert char_count("a b a") == {"a": 2, "b": 1}
    assert char_count("") == {}
