#!/usr/bin/env python3
"""
Commit-Gotchi 👾
A charming terminal virtual pet that thrives on your Git commits!
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

# Fix Windows console UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

STATE_FILE = Path.home() / ".commit_gotchi_state.json"

PETS = {
    "cat": {
        "name": "Neko",
        "species": "Cat",
        "godmode": [
            r"    /\_/\   🔥 GOD MODE 🔥",
            r"   (⌐■_■)  Commits: {commits} today!",
            r"  =(  ^  )=  LEVEL: MAXIMUM OVERDRIVE!",
            r"    U   U",
        ],
        "super_happy": [
            r"    /\_/\   ✨ HAPPY & ENERGIZED ✨",
            r"   (^ ‿ ^)  Commits: {commits} today",
            r"  =(  ^  )=  Purr... Delicious commits!",
            r"    U   U",
        ],
        "happy": [
            r"    /\_/\ ",
            r"   (• ‿ •)  Commits: {commits} today",
            r"  =(  .  )=  Nice work! Keep going!",
            r"    U   U",
        ],
        "hungry": [
            r"    /\_/\   💧 HUNGRY",
            r"   (╥ ﹏ ╥) Commits: 0 today",
            r"  =(  ~  )=  Please feed me code...",
            r"    U   U",
        ],
        "dead": [
            r"    /\_/\   💀 HIBERNATING",
            r"   (x . x)  Commits: 0 for days...",
            r"  =(  -  )=  *Ghostly meow*",
            r"    U   U",
        ],
    },
    "dino": {
        "name": "Rex",
        "species": "T-Rex",
        "godmode": [
            r"         __    ⚡ GOD MODE ⚡",
            r"       /⌐■_)   RAWR! {commits} COMMITS!",
            r"  .-^^^-/ /    I AM APEX DEVELOPER!",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "super_happy": [
            r"         __    ✨ FULL OF ENERGY ✨",
            r"       /(^‿_)  RAWR! {commits} commits!",
            r"  .-^^^-/ /    T-Rex is feasting well!",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "happy": [
            r"         __  ",
            r"       /(•‿_)  {commits} commits today",
            r"  .-^^^-/ /    Good job stomping bugs!",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "hungry": [
            r"         __    💧 STARVING",
            r"       /(╥﹏_) 0 commits today",
            r"  .-^^^-/ /    Stomach rumbling...",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
        "dead": [
            r"         __    💀 EXTINCT",
            r"       /(x._)  No commits in sight",
            r"  .-^^^-/ /    Turned into a fossil...",
            r" __/       / ",
            r"<__.|_|-|_|  ",
        ],
    },
    "crab": {
        "name": "Ferris",
        "species": "Rust Crab",
        "godmode": [
            r"     (\_/)     🦀 MAXIMUM CRAB POWER 🦀",
            r"    (⌐■_■)    {commits} COMMITS! ZERO COST!",
            r"   /|  ⚡  |\  Memory safe & blazing fast!",
            r"  / |_|_|_| \ ",
        ],
        "super_happy": [
            r"     (\_/)     ✨ CRAB PARTY ✨",
            r"    (^ ‿ ^)   {commits} commits today!",
            r"   /|  🦀  |\  *Happy clacking sounds*",
            r"  / |_|_|_| \ ",
        ],
        "happy": [
            r"     (\_/)   ",
            r"    (• ‿ •)   {commits} commits today",
            r"   /|     |\   Clack clack! Nice code!",
            r"  / |_|_|_| \ ",
        ],
        "hungry": [
            r"     (\_/)     💧 HUNGRY CRAB",
            r"    (╥ ﹏ ╥)  0 commits today",
            r"   /|  ~  |\   Rust compiler is sad...",
            r"  / |_|_|_| \ ",
        ],
        "dead": [
            r"     (\_/)     💀 BOILED CRAB",
            r"    (x . x)   0 commits for days",
            r"   /|  -  |\   Segmentation fault...",
            r"  / |_|_|_| \ ",
        ],
    },
}

QUOTES_GODMODE = [
    "🔥 20+ COMMITS TODAY! Your GitHub heatmap is blinding everyone!",
    "🚀 Keyboard on fire! Legendary productivity detected!",
    "⚡ Absolute 10x developer energy! Nothing can stop you!",
    "⭐ The green graph is singing your praises!",
]

QUOTES_HAPPY = [
    "✨ You pushed commits! I am feeling strong and full!",
    "💻 Great code today! My hunger meter is satisfied!",
    "🌟 Clean commits, clean code, happy pet!",
]

QUOTES_HUNGRY = [
    "🥺 Haven't seen a commit yet today... just a small one?",
    "🍕 Even 'git commit -m \"fix\"' counts as a snack!",
    "💭 Dreaming of fresh diffs and git pushes...",
]


def count_today_git_commits() -> int:
    """Scan current git repo or return 0 if not a repo or no commits today."""
    try:
        # Midnight today
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
        mood_label = "🔥 GODLIKE (10x Dev)"
        hunger = 100
        energy = 100
        quote = random.choice(QUOTES_GODMODE)
    elif commits >= 5:
        mood_key = "super_happy"
        mood_label = "✨ ECSTATIC"
        hunger = 95
        energy = 90
        quote = random.choice(QUOTES_HAPPY)
    elif commits >= 1:
        mood_key = "happy"
        mood_label = "😊 CONTENT"
        hunger = 70
        energy = 75
        quote = random.choice(QUOTES_HAPPY)
    else:
        mood_key = "hungry"
        mood_label = "🥺 STARVING"
        hunger = 15
        energy = 25
        quote = random.choice(QUOTES_HUNGRY)

    art_lines = pet_data[mood_key]
    happiness = min(100, state.get("happiness", 80))

    border_top = "╭" + "─" * 48 + "╮"
    border_bot = "╰" + "─" * 48 + "╯"

    print("\n" + border_top)
    print(f"│  👾 COMMIT-GOTCHI: {pet_data['name']} the {pet_data['species']}".ljust(49) + "│")
    print("├" + "─" * 48 + "┤")

    for line in art_lines:
        formatted = line.format(commits=commits)
        print(f"│  {formatted}".ljust(49) + "│")

    print("├" + "─" * 48 + "┤")
    print(f"│  Mood:       {mood_label}".ljust(49) + "│")
    print(f"│  Commits:    {commits} today".ljust(49) + "│")
    print(f"│  Satiety:    [{draw_bar(hunger)}] {hunger}%".ljust(49) + "│")
    print(f"│  Energy:     [{draw_bar(energy)}] {energy}%".ljust(49) + "│")
    print(f"│  Happiness:  [{draw_bar(happiness)}] {happiness}%".ljust(49) + "│")
    print("├" + "─" * 48 + "┤")
    print(f"│  💬 \"{quote}\"".ljust(49) + "│")
    print(border_bot + "\n")


def cmd_pet(state: dict, pet_type: str):
    state["happiness"] = min(100, state.get("happiness", 80) + 15)
    state["total_pets"] = state.get("total_pets", 0) + 1
    state["last_petted"] = datetime.datetime.now().isoformat()
    save_state(state)

    pet_name = PETS.get(pet_type, PETS["cat"])["name"]
    print(f"\n💖 You gently petted {pet_name}!")
    print(f"   {pet_name} purrs happily! (+15% Happiness)")
    print(f"   Total pats given: {state['total_pets']}\n")


def cmd_feed(state: dict, commits_add: int):
    state["bonus_commits"] = state.get("bonus_commits", 0) + commits_add
    state["happiness"] = min(100, state.get("happiness", 80) + 20)
    save_state(state)
    print(f"\n🍣 Fed {commits_add} tasty commit snack(s) to your gotchi!")
    print("   Nom nom nom! Burp! ✨\n")


def cmd_watch(pet_type: str, commits: int, state: dict):
    """Simple animated watch mode."""
    print("👀 Watching Commit-Gotchi... (Press Ctrl+C to exit)\n")
    frames = [
        "   (^ ‿ ^)  *wag wag*",
        "   (^ ‿ -)  *wink*",
        "   (• ‿ •)  *blink*",
        "   (⌐■_■)  *sunglasses shine*",
    ]
    try:
        while True:
            for f in frames:
                sys.stdout.write(f"\r  {f}  [Commits: {commits}] ")
                sys.stdout.flush()
                time.sleep(0.7)
    except KeyboardInterrupt:
        print("\n👋 See you soon!")


def main():
    parser = argparse.ArgumentParser(description="Commit-Gotchi: Terminal virtual pet powered by Git")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "pet", "feed", "watch", "reset"], help="Action to perform")
    parser.add_argument("--pet", choices=["cat", "dino", "crab"], default=None, help="Choose your pet companion")
    parser.add_argument("--commits", type=int, default=None, help="Simulate or override today's commit count")
    parser.add_argument("--feed-snack", type=int, default=1, help="Number of snacks to feed with 'feed'")

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
        print("🔄 State reset to defaults.")


if __name__ == "__main__":
    main()
