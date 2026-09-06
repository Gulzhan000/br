"""Консольная игра «Взломщик кода» на 10 ходов.

Игрок должен угадать секрет из четырёх разных цифр. После каждого хода
программа сообщает число «быков» (цифра и позиция угаданы) и «коров»
(цифра есть в коде, но стоит на другой позиции).
"""

from __future__ import annotations

import random
from collections.abc import Callable


CODE_LENGTH = 4
MAX_TURNS = 10


def generate_secret(rng: random.Random | None = None) -> str:
    """Создать секретный код из четырёх неповторяющихся цифр."""
    generator = rng or random.Random()
    return "".join(generator.sample("0123456789", CODE_LENGTH))


def validate_guess(guess: str) -> tuple[bool, str]:
    """Проверить введённый код и вернуть результат с пояснением."""
    if len(guess) != CODE_LENGTH:
        return False, "Введите ровно 4 цифры."
    if not guess.isdigit():
        return False, "Код должен состоять только из цифр."
    if len(set(guess)) != CODE_LENGTH:
        return False, "Цифры в коде не должны повторяться."
    return True, ""


def evaluate_guess(secret: str, guess: str) -> tuple[int, int]:
    """Вернуть количество быков и коров для корректной попытки."""
    bulls = sum(expected == actual for expected, actual in zip(secret, guess))
    cows = len(set(secret) & set(guess)) - bulls
    return bulls, cows


def play_game(
    secret: str | None = None,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> bool:
    """Провести игру и вернуть True при победе, иначе False.

    Некорректный ввод не расходует ход. Передача ``secret`` и функций
    ввода/вывода делает игровой сценарий полностью проверяемым в тестах.
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
