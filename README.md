# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/skyleradi/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/skyleradi/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4 KB of Python for make.fun's bounty "Build the strongest
chess engine in 4 KB of Python". 10x12 mailbox board, iterative deepening
with PVS, null-move pruning, LMR, transposition table and killers, tapered
PeSTO-style piece-square evaluation, mate-drive endgame term, and a
deterministic fixed node budget (no wall clock). `main.py` is a packed
entrypoint (LZMA payload written by `makefun compress`); the readable
source is `engine_src.py`.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8099 python3.13 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
