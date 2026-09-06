import random

import pytest
from codebreaker import evaluate_guess, generate_secret, play_game, validate_guess


@pytest.mark.parametrize(
    ("guess", "expected"),
    [
        ("1234", (True, "")),
        ("123", (False, "Введите ровно 4 цифры.")),
        ("12a4", (False, "Код должен состоять только из цифр.")),
        ("1123", (False, "Цифры в коде не должны повторяться.")),
    ],
)
def test_validate_guess(guess, expected):
    assert validate_guess(guess) == expected

@pytest.mark.parametrize(
    ("secret", "guess", "expected"),
    [
        ("1234", "1234", (4, 0)),
        ("1234", "4321", (0, 4)),
        ("1234", "1567", (1, 0)),
        ("1234", "2145", (0, 3)),
        ("1234", "5678", (0, 0)),
    ],
)
def test_evaluate_guess(secret, guess, expected):
    assert evaluate_guess(secret, guess) == expected


def test_generate_secret_has_four_unique_digits():
    secret = generate_secret(random.Random(42))
    assert len(secret) == 4
    assert secret.isdigit()
    assert len(set(secret)) == 4


def test_player_wins_on_tenth_turn():
    guesses = iter(["5678"] * 9 + ["1234"])
    messages = []

    result = play_game(
        secret="1234",
        input_func=lambda _: next(guesses),
        output_func=messages.append,
    )

    assert result is True
    assert messages[-1] == "Победа! Код 1234 разгадан за 10 ход(а)."


def test_player_loses_after_ten_turns():
    guesses = iter(["5678"] * 10)
    messages = []

    result = play_game(
        secret="1234",
        input_func=lambda _: next(guesses),
        output_func=messages.append,
    )

    assert result is False
    assert messages[-1] == "Ходы закончились. Секретный код: 1234."


def test_invalid_input_does_not_spend_a_turn():
    prompts = []
    guesses = iter(["11", "1234"])

    result = play_game(
        secret="1234",
        input_func=lambda prompt: prompts.append(prompt) or next(guesses),
        output_func=lambda _: None,
    )

    assert result is True
    assert prompts == ["Ход 1/10. Ваш код: ", "Ход 1/10. Ваш код: "]
