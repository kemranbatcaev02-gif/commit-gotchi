#!/usr/bin/env python3
"""
Commit-Gotchi 👾
Очаровательный виртуальный питомец в терминале, питающийся вашими коммитами в Git!
"""

import argparse
import datetime
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

# Поддержка UTF-8 на консолях Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

STATE_FILE = Path.home() / ".commit_gotchi_state.json"

PETS = {
    "cat": {
        "name": "Neko",
        "species": "Котик",
        "godmode": [
            r"    /\_/\   🔥 РЕЖИМ БОГА 🔥",
            r"   (⌐■_■)  Коммитов сегодня: {commits}!",
            r"  =(  ^  )=  УРОВЕНЬ: МАКСИМАЛЬНЫЙ РАЗГОН!",
            r"    U   U",
        ],
        "super_happy": [
            r"    /\_/\   ✨ СЫТЫЙ И СЧАСТЛИВЫЙ ✨",
            r"   (^ ‿ ^)  Коммитов сегодня: {commits}",
            r"  =(  ^  )=  Мурр... Вкуснейшие коммиты!",
            r"    U   U",
        ],
        "happy": [
            r"    /\_/\ ",
            r"   (• ‿ •)  Коммитов сегодня: {commits}",
            r"  =(  .  )=  Хорошая работа! Пиши ещё код!",
            r"    U   U",
        ],
        "hungry": [
            r"    /\_/\   💧 ГОЛОДАЕТ",
            r"   (╥ ﹏ ╥) Коммитов сегодня: 0",
            r"  =(  ~  )=  Пожалуйста, покорми меня кодом...",
            r"    U   U",
        ],
        "dead": [
            r"    /\_/\   💀 В СПЯЧКЕ",
            r"   (x . x)  Ни одного коммита за дни...",
            r"  =(  -  )=  *Призрачное мяу*",
            r"    U   U",
        ],
    },
    "dino": {
        "name": "Rex",
        "species": "Тираннозавр",
        "godmode": [
            r"         __    ⚡ РЕЖИМ БОГА ⚡",
            r"       /⌐■_)   РРРАВР! {commits} КОММИТОВ!",
            r"  .-^^^-/ /    Я ВЕРШИНА ЭВОЛЮЦИИ ДЕВЕЛОПЕРОВ!",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "super_happy": [
            r"         __    ✨ ПОЛОН ЭНЕРГИИ ✨",
            r"       /(^‿_)  РРРАВР! {commits} коммитов!",
            r"  .-^^^-/ /    Динозавр сыт и доволен!",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "happy": [
            r"         __  ",
            r"       /(•‿_)  {commits} коммитов сегодня",
            r"  .-^^^-/ /    Отлично растаптываешь баги!",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "hungry": [
            r"         __    💧 ГОЛОДНЫЙ ХИЩНИК",
            r"       /(╥﹏_) 0 коммитов сегодня",
            r"  .-^^^-/ /    В животе урчит...",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "dead": [
            r"         __    💀 ВЫМЕРШИЙ",
            r"       /(x._)  Никаких коммитов",
            r"  .-^^^-/ /    Окаменел от тоски...",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
    },
    "crab": {
        "name": "Ferris",
        "species": "Rust-Краб",
        "godmode": [
            r"     (\_/)     🦀 МАКСИМАЛЬНАЯ МОЩЬ RUST 🦀",
            r"    (⌐■_■)    {commits} КОММИТОВ! БЕЗ ОВЕРХЕДА!",
            r"   /|  ⚡  |\  Безопасная память и дикая скорость!",
            r"  / |_|_|_| \ ",
        ],
        "super_happy": [
            r"     (\_/)     ✨ КЛЕШНЕВАЯ ВЕЧЕРИНКА ✨",
            r"    (^ ‿ ^)   {commits} коммитов сегодня!",
            r"   /|  🦀  |\  *Радостное щёлканье клешнями*",
            r"  / |_|_|_| \ ",
        ],
        "happy": [
            r"     (\_/)   ",
            r"    (• ‿ •)   {commits} коммитов сегодня",
            r"   /|     |\   Клак-клак! Отличный код!",
            r"  / |_|_|_| \ ",
        ],
        "hungry": [
            r"     (\_/)     💧 ГОЛОДНЫЙ КРАБИК",
            r"    (╥ ﹏ ╥)  0 коммитов сегодня",
            r"   /|  ~  |\   Компилятор Rust грустит...",
            r"  / |_|_|_| \ ",
        ],
        "dead": [
            r"     (\_/)     💀 ВАРЕНЫЙ КРАБ",
            r"    (x . x)   0 коммитов за дни",
            r"   /|  -  |\   Segmentation fault...",
            r"  / |_|_|_| \ ",
        ],
    },
    "dog": {
        "name": "Shiba",
        "species": "Сиба-ину",
        "godmode": [
            r"    / \__      🐕 СТОЛЬКО КОММИТОВ! ВАУ! 🐕",
            r"   (    ⌐■\___ {commits} КОММИТОВ! ТАКОЙ СЕНЬОР!",
            r"   /  ⚡      O СВЕРХСКОРОСТНОЙ ДЕПЛОЙ!",
            r"  /   (_____/ ",
            r" /_____/   U  ",
        ],
        "super_happy": [
            r"    / \__      ✨ СЧАСТЛИВЫЙ ДОГЕ ✨",
            r"   (    ^ \___ {commits} коммитов сегодня! Гав!",
            r"   /  💖      O *Хвост виляет на сверхзвуковой скорости*",
            r"  /   (_____/ ",
            r" /_____/   U  ",
        ],
        "happy": [
            r"    / \__     ",
            r"   (    • \___ {commits} коммитов сегодня",
            r"   /          O Гав! Отличная работа, человек!",
            r"  /   (_____/ ",
            r" /_____/   U  ",
        ],
        "hungry": [
            r"    / \__      💧 ГОЛОДНЫЙ ПЁСИК",
            r"   (    ╥ \___ 0 коммитов сегодня",
            r"   /  ~       O *Тихонько скулит и просит код*",
            r"  /   (_____/ ",
            r" /_____/   U  ",
        ],
        "dead": [
            r"    / \__      💀 СПЯЩИЙ ДОГЕ",
            r"   (    x \___ 0 коммитов за много дней",
            r"   /          O Хрр... Спит и видит git push",
            r"  /   (_____/ ",
            r" /_____/   U  ",
        ],
    },
}

QUOTES_GODMODE = [
    "🔥 20+ коммитов сегодня! Твой график активности на GitHub ослепляет всех!",
    "🚀 Клавиатура пылает! Зафиксирована легендарная продуктивность!",
    "⚡ Энергия абсолютного 10x разработчика! Тебя не остановить!",
    "⭐ Зеленый график на GitHub поет тебе дифирамбы!",
]

QUOTES_HAPPY = [
    "✨ Свежие коммиты! Питомец полон сил и энергии!",
    "💻 Отличный код сегодня! Шкала сытости удовлетворена!",
    "🌟 Чистые коммиты, аккуратный код, счастливый питомец!",
]

QUOTES_HUNGRY = [
    "🥺 Сегодня еще не было коммитов... хотя бы один маленький?",
    "🍕 Даже 'git commit -m \"fix\"' сойдет за вкусный перекус!",
    "💭 Питомец мечтает о свежих диффах и пушах в репозиторий...",
]


def count_today_git_commits() -> int:
    """Scan current git repo or return 0 if not a repo or no commits today."""
    try:
        today_midnight = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        res = subprocess.run(
            ["git", "log", f"--since={today_midnight}", "--oneline"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if res.returncode == 0:
            lines = [l for l in res.stdout.strip().splitlines() if l.strip()]
            return len(lines)
    except Exception:
        pass
    return 0


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "pet": "cat",
        "happiness": 80,
        "bonus_commits": 0,
        "last_petted": None,
        "total_pets": 0,
    }


def save_state(state: dict):
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass


def draw_bar(val: int, max_val: int = 100, width: int = 16) -> str:
    filled = max(0, min(width, int((val / max_val) * width)))
    empty = width - filled
    return "█" * filled + "░" * empty


def render_card(pet_type: str, commits: int, state: dict):
    pet_data = PETS.get(pet_type, PETS["cat"])

    # Determine mood
    if commits >= 20:
        mood_key = "godmode"
        mood_label = "🔥 БОЖЕСТВЕННОЕ (10x Dev)"
        hunger = 100
        energy = 100
        quote = random.choice(QUOTES_GODMODE)
    elif commits >= 5:
        mood_key = "super_happy"
        mood_label = "✨ ВОСТОРГ"
        hunger = 95
        energy = 90
        quote = random.choice(QUOTES_HAPPY)
    elif commits >= 1:
        mood_key = "happy"
        mood_label = "😊 ДОВОЛЕН"
        hunger = 70
        energy = 75
        quote = random.choice(QUOTES_HAPPY)
    else:
        mood_key = "hungry"
        mood_label = "🥺 ГОЛОДАЕТ"
        hunger = 15
        energy = 25
        quote = random.choice(QUOTES_HUNGRY)

    art_lines = pet_data[mood_key]
    happiness = min(100, state.get("happiness", 80))

    border_top = "╭" + "─" * 48 + "╮"
    border_bot = "╰" + "─" * 48 + "╯"

    print("\n" + border_top)
    header = f"│  👾 COMMIT-GOTCHI: {pet_data['name']} ({pet_data['species']})"
    print(header.ljust(49) + "│")
    print("├" + "─" * 48 + "┤")

    for line in art_lines:
        formatted = line.format(commits=commits)
        print(f"│  {formatted}".ljust(49) + "│")

    print("├" + "─" * 48 + "┤")
    print(f"│  Настроение: {mood_label}".ljust(49) + "│")
    print(f"│  Коммитов:   {commits} сегодня".ljust(49) + "│")
    print(f"│  Сытость:    [{draw_bar(hunger)}] {hunger}%".ljust(49) + "│")
    print(f"│  Энергия:    [{draw_bar(energy)}] {energy}%".ljust(49) + "│")
    print(f"│  Счастье:    [{draw_bar(happiness)}] {happiness}%".ljust(49) + "│")
    print("├" + "─" * 48 + "┤")
    print(f"│  💬 \"{quote}\"".ljust(49) + "│")
    print(border_bot + "\n")


def cmd_pet(state: dict, pet_type: str):
    state["happiness"] = min(100, state.get("happiness", 80) + 15)
    state["total_pets"] = state.get("total_pets", 0) + 1
    state["last_petted"] = datetime.datetime.now().isoformat()
    save_state(state)

    pet_name = PETS.get(pet_type, PETS["cat"])["name"]
    print(f"\n💖 Вы нежно погладили {pet_name}!")
    print(f"   {pet_name} довольно мурлычет! (+15% к Счастью)")
    print(f"   Всего поглаживаний: {state['total_pets']}\n")


def cmd_feed(state: dict, commits_add: int):
    state["bonus_commits"] = state.get("bonus_commits", 0) + commits_add
    state["happiness"] = min(100, state.get("happiness", 80) + 20)
    save_state(state)
    print(f"\n🍣 Вы скормили {commits_add} вкусный(х) коммит-снек(ов)!")
    print("   Ням-ням-ням! Питомец сыт и благодарен! ✨\n")


def cmd_watch(pet_type: str, commits: int, state: dict):
    """Simple animated watch mode."""
    print("👀 Наблюдаем за Commit-Gotchi... (Нажмите Ctrl+C для выхода)\n")
    frames = [
        "   (^ ‿ ^)  *виляет хвостиком*",
        "   (^ ‿ -)  *подмигивает*",
        "   (• ‿ •)  *моргает*",
        "   (⌐■_■)  *поправляет очки*",
    ]
    try:
        while True:
            for f in frames:
                sys.stdout.write(f"\r  {f}  [Коммитов: {commits}] ")
                sys.stdout.flush()
                time.sleep(0.7)
    except KeyboardInterrupt:
        print("\n👋 До скорой встречи!")


def main():
    parser = argparse.ArgumentParser(description="Commit-Gotchi: Виртуальный терминальный питомец, питающийся коммитами")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "pet", "feed", "watch", "reset"], help="Действие с питомцем")
    parser.add_argument("--pet", choices=["cat", "dino", "crab", "dog"], default=None, help="Выбрать вид питомца")
    parser.add_argument("--commits", type=int, default=None, help="Симулировать или задать количество коммитов на сегодня")
    parser.add_argument("--feed-snack", type=int, default=1, help="Количество снеков для команды 'feed'")

    args = parser.parse_args()
    state = load_state()

    if args.pet:
        state["pet"] = args.pet
        save_state(state)

    active_pet = state.get("pet", "cat")

    # Determine commit count
    if args.commits is not None:
        today_commits = args.commits
    else:
        today_commits = count_today_git_commits() + state.get("bonus_commits", 0)

    if args.command == "status":
        render_card(active_pet, today_commits, state)
    elif args.command == "pet":
        cmd_pet(state, active_pet)
        render_card(active_pet, today_commits, state)
    elif args.command == "feed":
        cmd_feed(state, args.feed_snack)
        today_commits += args.feed_snack
        render_card(active_pet, today_commits, state)
    elif args.command == "watch":
        cmd_watch(active_pet, today_commits, state)
    elif args.command == "reset":
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("🔄 Настройки сброшены к начальным значениям.")


if __name__ == "__main__":
    main()
