# chess-engine-4kb

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Jsmile19/chess-engine-4kb/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Jsmile19/chess-engine-4kb/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A tiny deterministic chess engine in under 4 KB of Python: 0x88 board, negamax with alpha-beta, quiescence search, transposition table and iterative deepening on a fixed node budget. It plays the house gauntlet over HTTP with no clock, no randomness and no model calls, so every trial replays move-for-move.

## Run it

```sh
MAKEFUN_ENV_URL=<game-server-url> python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=q3bse5cn&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
