import math
import random

LEVELS = {
    "easy":   {"root_lo": 2, "root_hi": 7,  "percent": 10, "precision": 0.1,   "name":"🟢 Лёгкий",  "time_limit":60},
    "medium": {"root_lo": 5, "root_hi": 10, "percent": 25, "precision": 0.01,  "name":"🟡 Средний", "time_limit":90},
    "hard":   {"root_lo": 7, "root_hi": 15, "percent": 40, "precision": 0.001, "name":"🔴 Сложный", "time_limit":120},
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

def get_next_level(total_done: int, correct: int) -> str:
    if total_done < 3:
        return "easy"
    elif total_done < 6:
        return "medium"
    elif total_done < 9:
        return "hard"
    winrate = correct / total_done if total_done > 0 else 0
    if winrate > 0.7:
        return "hard"
    elif winrate>= 0.3:
        return "medium"
    else:
        return "easy"