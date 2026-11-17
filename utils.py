import math
import random

LEVELS = {
    "easy":   {"root_lo": 2, "root_hi": 7,  "percent": 10, "precision": 0.1,   "name":"🟢 Лёгкий"},
    "medium": {"root_lo": 5, "root_hi": 10, "percent": 25, "precision": 0.01,  "name":"🟡 Средний"},
    "hard":   {"root_lo": 7, "root_hi": 15, "percent": 40, "precision": 0.001, "name":"🔴 Сложный"},
}


def generate_task(level: str) -> dict:
    cfg = LEVELS[level]
    while True:
        root = random.randint(cfg['root_lo'],cfg["root_hi"])
        lower = root ** 2
        upper = (root + 1) ** 2
        gap = upper - lower

        max_dist = max(1, round(gap*cfg["percent"] / 100))
        dist = random.randint(1, max_dist)
        number = lower + dist

        if math.isqrt(number) ** 2 != number:
            return {
                "number" : number,
                "precision": cfg["precision"],
                "level": level,
            }


def check_answer(user_answer: float, task: dict) -> bool:
    correct = math.sqrt(task["number"])
    return abs(user_answer - correct) <= task["precision"]


def correct_answer(task: dict) -> float:
    return math.sqrt(task["number"])

def get_callibration_level(total_done: int) -> str:
    if total_done < 3:
        return "easy"
    elif total_done < 6:
        return "medium"
    else:
        return "hard"