# 👾 Commit-Gotchi

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge" alt="Zero Dependencies"/>
  <img src="https://img.shields.io/badge/Vibe-10x%20Developer-orange?style=for-the-badge" alt="Vibe"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License"/>
</p>

> A charming terminal virtual pet that feeds on your Git commits! Keeps you motivated, happy, and shipping code. 🚀

---

## 📺 Terminal Demo

```text
╭────────────────────────────────────────────────╮
│  👾 COMMIT-GOTCHI: Neko the Cat                │
├────────────────────────────────────────────────┤
│      /\_/\   🔥 GOD MODE 🔥                     │
│     (⌐■_■)  Commits: 20 today!                 │
│    =(  ^  )=  LEVEL: MAXIMUM OVERDRIVE!        │
│      U   U                                     │
├────────────────────────────────────────────────┤
│  Mood:       🔥 GODLIKE (10x Dev)              │
│  Commits:    20 today                          │
│  Satiety:    [████████████████] 100%           │
│  Energy:     [████████████████] 100%           │
│  Happiness:  [███████████████░] 95%            │
├────────────────────────────────────────────────┤
│  💬 "🚀 Keyboard on fire! Legendary productivity detected!"│
╰────────────────────────────────────────────────╯
```

---

## ✨ Features

- 🐾 **Multiple Pets**:
  - 🐱 **Neko the Cat**: Loves snacks and cozy commits.
  - 🦖 **Rex the T-Rex**: Smashes bugs with primal rawr power.
  - 🦀 **Ferris the Crab**: Memory safe and blazing fast.
- ⚡ **Auto-detects Today's Commits**: Automatically reads `git log --since="midnight"` from your active repo.
- 🔥 **Mood & Health States**:
  - `🔥 GOD MODE` (20+ commits): Sunglasses on, max energy, pure 10x developer aura!
  - `✨ ECSTATIC` (5–19 commits): Well-fed and energized.
  - `😊 CONTENT` (1–4 commits): Healthy and happy.
  - `💧 STARVING` (0 commits): Pleads for you to push some code.
  - `💀 EXTINCT / SLEEPING` (inactive): Hibernates until you code again.
- 🖐️ **Interactive Actions**:
  - `gotchi pet`: Pat your pet to boost happiness.
  - `gotchi feed`: Treat it with snacks.
  - `gotchi watch`: Real-time animated terminal buddy.
- 📦 **Zero External Dependencies**: Standard Python library only!

---

## 🚀 Quick Start

### 1. Check Pet Status
```bash
python gotchi.py status
```

### 2. Choose Your Pet
```bash
python gotchi.py --pet cat
python gotchi.py --pet dino
python gotchi.py --pet crab
```

### 3. Interact with Your Pet
```bash
# Pet your gotchi (raises happiness!)
python gotchi.py pet

# Feed a commit snack
python gotchi.py feed

# Watch live animations
python gotchi.py watch
```

### 4. Test Different Moods
```bash
# Simulate 20 commits for God Mode:
python gotchi.py status --commits 20

# Simulate 0 commits:
python gotchi.py status --commits 0
```

---

## 💡 Shell Integration (Fun Tip!)

Want your pet to greet you every time you open a terminal or push code?
Add this alias to your `.bashrc` or PowerShell `$PROFILE`:

```powershell
# PowerShell:
function gotchi { python path\to\commit-gotchi\gotchi.py @args }
```

Or run it as a Git `post-commit` hook!

---

## 🧪 Testing

```bash
python -m unittest discover -s tests
```

---

## 📜 License

MIT License. Free to star and share! ⭐
