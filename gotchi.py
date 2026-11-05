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
    "duck": {
        "name": "Ducky",
        "species": "Резиновая уточка",
        "godmode": [
            r"      __       🦆 РЕЖИМ БОГА ДЕБАГА 🦆",
            r"   <(o )___-  (⌐■_■) {commits} КОММИТОВ!",
            r"    ( ._> /    КРЯ! ВСЕ БАГИ УНИЧТОЖЕНЫ!",
            r"     `---' ",
        ],
        "super_happy": [
            r"      __       ✨ КРЯ-ВЕЧЕРИНКА ✨",
            r"   <(o )___-  (^ ‿ ^) {commits} коммитов!",
            r"    ( ._> /    Метод уточки творит чудеса!",
            r"     `---' ",
        ],
        "happy": [
            r"      __     ",
            r"   <(• )___-  (• ‿ •) {commits} коммитов",
            r"    ( ._> /    Кря! Расскажи мне про свой код!",
            r"     `---' ",
        ],
        "hungry": [
            r"      __       💧 ГРУСТНАЯ УТОЧКА",
            r"   <(╥ )___-  0 коммитов сегодня",
            r"    ( ._> /    *Тихое тоскливое кряканье...*",
            r"     `---' ",
        ],
        "dead": [
            r"      __       💀 УТОНУЛА",
            r"   <(x )___-  0 коммитов за дни",
            r"    ( ._> /    Ушла на дно ванной...",
            r"     `---' ",
        ],
    },
    "dragon": {
        "name": "Ignis",
        "species": "Огненный Дракон",
        "godmode": [
            r"     / \   / \   🔥 ДРЕВНИЙ ДРАКОН ПРОДАКШЕНА 🔥",
            r"    ( >.< )-( >.< ) {commits} КОММИТОВ! ДЫШИТ ОГНЕМ!",
            r"   <  \  /   \  / > КЛАВИАТУРА ИСПАРИЛАСЬ В ПЕПЕЛ!",
            r"    ===v=======v=== ",
        ],
        "super_happy": [
            r"     / \   / \   ✨ ВЛАДЫКА РЕПОЗИТОРИЯ ✨",
            r"    ( ^.^ )-( ^.^ ) {commits} коммитов сегодня!",
            r"   <  \  /   \  / > Дремлет на золотых мерджах...",
            r"    ===v=======v=== ",
        ],
        "happy": [
            r"     / \   / \  ",
            r"    ( •.• )-( •.• ) {commits} коммитов сегодня",
            r"   <  \  /   \  / > Сытое урчание и снопы искр!",
            r"    ===v=======v=== ",
        ],
        "hungry": [
            r"     / \   / \   💧 ГОЛОДНЫЙ ДРАКОН",
            r"    ( ╥.╥ )-( ╥.╥ ) 0 коммитов сегодня",
            r"   <  \  /   \  / > Чешуя тускнеет без коммитов...",
            r"    ===v=======v=== ",
        ],
        "dead": [
            r"     / \   / \   💀 В ВЕКОВОЙ СПЯЧКЕ",
            r"    ( x.x )-( x.x ) Никаких коммитов...",
            r"   <  \  /   \  / > Окаменел в глубокой пещере.",
            r"    ===v=======v=== ",
        ],
    },
    "owl": {
        "name": "Archie",
        "species": "Сыч-Архитектор",
        "godmode": [
            r"     {o,o}   🦉 ЛЕГЕНДАРНЫЙ НОЧНОЙ СЫЧ 🦉",
            r"     (⌐■_■)  {commits} КОММИТОВ! 3:00 AM DEPLOY!",
            r"     --\"--\"- ВСЕ БАГИ ВИДНЫ В ТЕМНОТЕ!",
            r"       ===   ",
        ],
        "super_happy": [
            r"     {o,o}   ✨ МУДРЫЙ И СЫТЫЙ ✨",
            r"     (^ ‿ ^) {commits} коммитов сегодня!",
            r"     --\"--\"- Уху-уху! Изящная архитектура!",
            r"       ===   ",
        ],
        "happy": [
            r"     {o,o}  ",
            r"     (• ‿ •) {commits} коммитов сегодня",
            r"     --\"--\"- Уху! Чистый код и ровные диффы!",
            r"       ===   ",
        ],
        "hungry": [
            r"     {o,o}   💧 НЕДОСЫП И ГОЛОД",
            r"     (╥ ﹏ ╥) 0 коммитов сегодня",
            r"     --\"--\"- Кофе остыл, коммитов нет...",
            r"       ===   ",
        ],
        "dead": [
            r"     {x,x}   💀 СВАЛИЛСЯ С ВЕТКИ",
            r"     (x . x) 0 коммитов за дни",
            r"     --\"--\"- Хрр... Спит до следующего спринта.",
            r"       ===   ",
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

LEVEL_RANKS = [
    (1, 0, "🐣 Intern Coder"),
    (2, 25, "🌱 Junior Dev"),
    (3, 75, "⚡ Middle Engineer"),
    (4, 150, "🔥 Senior Architect"),
    (5, 300, "👑 Lead Tech Guru"),
    (6, 600, "🌟 Mythic 10x Legend"),
]

ACHIEVEMENTS = [
    {
        "id": "first_blood",
        "title": "🩸 Первый коммит",
        "desc": "Сделать свой первый коммит сегодня (>=1)",
        "check": lambda c, st, s: c >= 1
    },
    {
        "id": "streak_3",
        "title": "🔥 В огне (3 дня)",
        "desc": "Удерживать непрерывный стрик от 3 дней",
        "check": lambda c, st, s: st >= 3
    },
    {
        "id": "streak_7",
        "title": "⚡ Недельный марафон",
        "desc": "Удерживать стрик коммитов 7+ дней подряд",
        "check": lambda c, st, s: st >= 7
    },
    {
        "id": "pet_lover",
        "title": "💖 Пушистый релакс",
        "desc": "Погладить питомца не менее 5 раз",
        "check": lambda c, st, s: s.get("total_pets", 0) >= 5
    },
    {
        "id": "snack_master",
        "title": "🍣 Гурман снеков",
        "desc": "Скормить питомцу 3+ бонусных коммит-снека",
        "check": lambda c, st, s: s.get("bonus_commits", 0) >= 3
    },
    {
        "id": "godmode",
        "title": "👑 Божественный режим",
        "desc": "Набрать 20+ коммитов за один рабочий день",
        "check": lambda c, st, s: c >= 20
    },
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


def calculate_git_streak() -> int:
    """Calculates current streak of consecutive days with commits."""
    try:
        res = subprocess.run(
            ["git", "log", "--date=short", "--format=%ad"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if res.returncode == 0 and res.stdout.strip():
            unique_dates = sorted(
                list({datetime.date.fromisoformat(line.strip()) for line in res.stdout.splitlines() if line.strip()}),
                reverse=True
            )
            if not unique_dates:
                return 0

            today = datetime.date.today()
            streak = 0
            current_check = today

            if unique_dates[0] < today:
                if unique_dates[0] == today - datetime.timedelta(days=1):
                    current_check = today - datetime.timedelta(days=1)
                else:
                    return 0

            for d in unique_dates:
                if d == current_check:
                    streak += 1
                    current_check -= datetime.timedelta(days=1)
                elif d < current_check:
                    break
            return max(1, streak)
    except Exception:
        pass
    return 1


def calculate_xp_and_level(state: dict, today_commits: int) -> tuple[int, int, str, int, int]:
    """Returns (xp, level, rank_title, cur_base, next_goal)"""
    total_xp = (
        state.get("lifetime_commits", 0)
        + today_commits
        + state.get("bonus_commits", 0) * 2
        + state.get("total_pets", 0) * 3
    )
    level = 1
    rank = LEVEL_RANKS[0][2]
    cur_base = 0
    next_goal = LEVEL_RANKS[1][1]

    for lvl, threshold, title in LEVEL_RANKS:
        if total_xp >= threshold:
            level = lvl
            rank = title
            cur_base = threshold
        else:
            next_goal = threshold
            break
    else:
        next_goal = cur_base + 300

    return total_xp, level, rank, cur_base, next_goal


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
        "lifetime_commits": 35,
    }


def save_state(state: dict):
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass


def draw_bar(val: int, max_val: int = 100, width: int = 16) -> str:
    if max_val <= 0:
        return "░" * width
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
    streak_val = calculate_git_streak()
    if commits > 0 and streak_val == 0:
        streak_val = 1

    total_xp, level, rank_title, cur_base, next_goal = calculate_xp_and_level(state, commits)
    span = max(1, next_goal - cur_base)
    prog = max(0, min(span, total_xp - cur_base))
    lvl_bar = draw_bar(prog, span, width=12)

    border_top = "╭" + "─" * 52 + "╮"
    border_bot = "╰" + "─" * 52 + "╯"

    print("\n" + border_top)
    header = f"│  👾 COMMIT-GOTCHI: {pet_data['name']} ({pet_data['species']})"
    print(header.ljust(53) + "│")
    print("├" + "─" * 52 + "┤")

    for line in art_lines:
        formatted = line.format(commits=commits)
        print(f"│  {formatted}".ljust(53) + "│")

    print("├" + "─" * 52 + "┤")
    print(f"│  Уровень:    LVL {level} [{lvl_bar}] {total_xp} XP".ljust(53) + "│")
    print(f"│  Ранг:       {rank_title}".ljust(53) + "│")
    print(f"│  Настроение: {mood_label}".ljust(53) + "│")
    print(f"│  Коммитов:   {commits} сегодня".ljust(53) + "│")
    print(f"│  Стрик:      {streak_val} дн. непрерывно 🔥".ljust(53) + "│")
    print(f"│  Сытость:    [{draw_bar(hunger)}] {hunger}%".ljust(53) + "│")
    print(f"│  Энергия:    [{draw_bar(energy)}] {energy}%".ljust(53) + "│")
    print(f"│  Счастье:    [{draw_bar(happiness)}] {happiness}%".ljust(53) + "│")
    print("├" + "─" * 52 + "┤")
    print(f"│  💬 \"{quote}\"".ljust(53) + "│")
    print(border_bot + "\n")


def cmd_pet(state: dict, pet_type: str):
    state["happiness"] = min(100, state.get("happiness", 80) + 15)
    state["total_pets"] = state.get("total_pets", 0) + 1
    state["last_petted"] = datetime.datetime.now().isoformat()
    save_state(state)

    pet_name = PETS.get(pet_type, PETS["cat"])["name"]
    print(f"\n💖 Вы нежно погладили {pet_name}!")
    print(f"   {pet_name} довольно мурлычет! (+15% к Счастью, +3 XP)")
    print(f"   Всего поглаживаний: {state['total_pets']}\n")


def cmd_feed(state: dict, commits_add: int):
    state["bonus_commits"] = state.get("bonus_commits", 0) + commits_add
    state["happiness"] = min(100, state.get("happiness", 80) + 20)
    save_state(state)
    print(f"\n🍣 Вы скормили {commits_add} вкусный(х) коммит-снек(ов)!")
    print("   Ням-ням-ням! Питомец сыт и благодарен! ✨\n")


def cmd_achievements(state: dict, today_commits: int):
    streak_val = calculate_git_streak()
    if today_commits > 0 and streak_val == 0:
        streak_val = 1

    border_top = "╭" + "─" * 56 + "╮"
    border_bot = "╰" + "─" * 56 + "╯"

    print("\n" + border_top)
    print("│  🏆 ДОСТИЖЕНИЯ И НАГРАДЫ COMMIT-GOTCHI".ljust(57) + "│")
    print("├" + "─" * 56 + "┤")

    unlocked_count = 0
    for ach in ACHIEVEMENTS:
        is_unlocked = ach["check"](today_commits, streak_val, state)
        if is_unlocked:
            unlocked_count += 1
            mark = "✅ [ОТКРЫТО]"
        else:
            mark = "🔒 [ЗАКРЫТО]"

        title_line = f"│  {mark} {ach['title']}"
        desc_line = f"│     └─ {ach['desc']}"
        print(title_line.ljust(57) + "│")
        print(desc_line.ljust(57) + "│")

    print("├" + "─" * 56 + "┤")
    print(f"│  Прогресс: {unlocked_count}/{len(ACHIEVEMENTS)} достижений разблокировано".ljust(57) + "│")
    print(border_bot + "\n")


def cmd_export_badge(state: dict, pet_type: str, today_commits: int, fmt: str):
    pet_data = PETS.get(pet_type, PETS["cat"])
    p_name = pet_data["name"]
    total_xp, level, rank_title, _, _ = calculate_xp_and_level(state, today_commits)

    clean_rank = rank_title.split()[-1]
    badge_label = f"Gotchi-{p_name}"
    badge_message = f"LVL_{level}_{clean_rank}"
    badge_url = f"https://img.shields.io/badge/{badge_label}-{badge_message}-orange?style=flat-square&logo=github"
    md_badge = f"[![Commit-Gotchi]({badge_url})](https://github.com/kemranbatcaev02-gif/commit-gotchi)"

    if fmt == "url":
        print(badge_url)
    elif fmt == "json":
        data = {
            "pet": p_name,
            "species": pet_data["species"],
            "level": level,
            "rank": rank_title,
            "xp": total_xp,
            "badge_url": badge_url,
            "markdown": md_badge,
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("\n📋 Скопируйте этот Markdown-код в свой GitHub README.md:\n")
        print(f"```markdown\n{md_badge}\n```\n")


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
    parser = argparse.ArgumentParser(
        description="Commit-Gotchi 👾: Виртуальный терминальный питомец, питающийся коммитами"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="status",
        choices=["status", "pet", "feed", "watch", "reset", "achievements", "export-badge"],
        help="Действие с питомцем",
    )
    parser.add_argument(
        "--pet",
        choices=["cat", "dino", "crab", "dog", "duck", "dragon", "owl"],
        default=None,
        help="Выбрать вид питомца",
    )
    parser.add_argument("--commits", type=int, default=None, help="Симулировать или задать количество коммитов на сегодня")
    parser.add_argument("--feed-snack", type=int, default=1, help="Количество снеков для команды 'feed'")
    parser.add_argument("--format", choices=["markdown", "url", "json"], default="markdown", help="Формат вывода для export-badge")

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
    elif args.command == "achievements":
        cmd_achievements(state, today_commits)
    elif args.command == "export-badge":
        cmd_export_badge(state, active_pet, today_commits, args.format)
    elif args.command == "watch":
        cmd_watch(active_pet, today_commits, state)
    elif args.command == "reset":
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        print("🔄 Настройки сброшены к начальным значениям.")


if __name__ == "__main__":
    main()
