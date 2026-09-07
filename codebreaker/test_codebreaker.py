"""Автоматические тесты игры «Взломщик кода» на pytest."""

import random

import pytest

from codebreaker import evaluate_guess, generate_secret, play_game, validate_guess


@pytest.mark.parametrize(
    ("guess", "expected"),
    [
        pytest.param("1234", (True, ""), id="valid"),
        pytest.param("0123", (True, ""), id="leading-zero"),
        pytest.param("", (False, "Введите ровно 4 цифры."), id="empty"),
        pytest.param("123", (False, "Введите ровно 4 цифры."), id="too-short"),
        pytest.param("12345", (False, "Введите ровно 4 цифры."), id="too-long"),
        pytest.param("12a4", (False, "Код должен состоять только из цифр от 0 до 9."), id="letter"),
        pytest.param("１２３４", (False, "Код должен состоять только из цифр от 0 до 9."), id="non-ascii-digits"),
        pytest.param("1123", (False, "Цифры в коде не должны повторяться."), id="repeated-digit"),
    ],
)
def test_validate_guess(guess: str, expected: tuple[bool, str]) -> None:
    """Корректный ввод принимается, некорректный — отклоняется с причиной."""
    assert validate_guess(guess) == expected


@pytest.mark.parametrize(
    ("secret", "guess", "expected"),
    [
        pytest.param("1234", "1234", (4, 0), id="four-bulls"),
        pytest.param("1234", "4321", (0, 4), id="four-cows"),
        pytest.param("1234", "1567", (1, 0), id="one-bull"),
        pytest.param("1234", "2145", (0, 3), id="three-cows"),
        pytest.param("1234", "5678", (0, 0), id="no-matches"),
    ],
)
def test_evaluate_guess(secret: str, guess: str, expected: tuple[int, int]) -> None:
    """Подсчёт быков и коров соответствует правилам игры."""
    assert evaluate_guess(secret, guess) == expected


def test_generate_secret_has_four_unique_ascii_digits() -> None:
    """Генератор создаёт код нужного формата."""
    secret = generate_secret(random.Random(42))
    assert len(secret) == 4
    assert all(symbol in "0123456789" for symbol in secret)
    assert len(set(secret)) == 4


def test_generate_secret_is_reproducible_with_seed() -> None:
    """Внедрённый генератор делает тест детерминированным."""
    assert generate_secret(random.Random(42)) == "1049"


def test_player_wins_on_tenth_turn() -> None:
    guesses = iter(["5678"] * 9 + ["1234"])
    messages: list[str] = []
    result = play_game(secret="1234", input_func=lambda _: next(guesses), output_func=messages.append)
    assert result is True
    assert messages[-1] == "Победа! Код 1234 разгадан за 10 ход(а)."


def test_player_loses_after_ten_turns() -> None:
    guesses = iter(["5678"] * 10)
    messages: list[str] = []
    result = play_game(secret="1234", input_func=lambda _: next(guesses), output_func=messages.append)
    assert result is False
    assert messages[-1] == "Ходы закончились. Секретный код: 1234."


def test_invalid_input_does_not_spend_a_turn() -> None:
    prompts: list[str] = []
    messages: list[str] = []
    guesses = iter(["11", "1234"])
    result = play_game(
        secret="1234",
        input_func=lambda prompt: prompts.append(prompt) or next(guesses),
        output_func=messages.append,
    )
    assert result is True
    assert prompts == ["Ход 1/10. Ваш код: ", "Ход 1/10. Ваш код: "]
    assert "Ошибка: Введите ровно 4 цифры." in messages
