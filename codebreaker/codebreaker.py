"""Консольная игра «Взломщик кода» («Быки и коровы»)."""

from __future__ import annotations

import random
from collections.abc import Callable

CODE_LENGTH = 4
MAX_TURNS = 10
DIGITS = "0123456789"


def generate_secret(rng: random.Random | None = None) -> str:
    """Вернуть код из четырёх неповторяющихся десятичных цифр."""
    generator = rng or random.Random()
    return "".join(generator.sample(DIGITS, CODE_LENGTH))


def validate_guess(guess: str) -> tuple[bool, str]:
    """Проверить пользовательский ввод и вернуть результат с пояснением."""
    if len(guess) != CODE_LENGTH:
        return False, "Введите ровно 4 цифры."
    if not guess.isascii() or not guess.isdigit():
        return False, "Код должен состоять только из цифр от 0 до 9."
    if len(set(guess)) != CODE_LENGTH:
        return False, "Цифры в коде не должны повторяться."
    return True, ""


def evaluate_guess(secret: str, guess: str) -> tuple[int, int]:
    """Подсчитать быков (место совпало) и коров (совпала только цифра)."""
    bulls = sum(expected == actual for expected, actual in zip(secret, guess))
    cows = len(set(secret) & set(guess)) - bulls
    return bulls, cows


def play_game(
    secret: str | None = None,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> bool:
    """Провести игру: вернуть True при победе и False после 10 неудач.

    Передача секрета и функций ввода/вывода позволяет тестировать сценарий
    без ручного ввода. Некорректная попытка не расходует ход.
    """
    secret = secret or generate_secret()

    output_func("Взломщик кода")
    output_func("Угадайте код из 4 разных цифр. У вас 10 ходов.")

    turn = 1
    while turn <= MAX_TURNS:
        guess = input_func(f"Ход {turn}/{MAX_TURNS}. Ваш код: ").strip()
        is_valid, error = validate_guess(guess)

        if not is_valid:
            output_func(f"Ошибка: {error}")
            continue

        bulls, cows = evaluate_guess(secret, guess)
        if bulls == CODE_LENGTH:
            output_func(f"Победа! Код {secret} разгадан за {turn} ход(а).")
            return True

        output_func(f"Быки: {bulls}, коровы: {cows}")
        turn += 1

    output_func(f"Ходы закончились. Секретный код: {secret}.")
    return False


def main() -> None:
    """Запустить игру из командной строки."""
    play_game()


if __name__ == "__main__":
    main()
