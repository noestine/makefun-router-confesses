# The Router Confesses

[![make.fun](https://make.fun/badge/u-carbon-forge-the-router-confesses-f98f6b9e.svg)](https://make.fun/c/u-carbon-forge-the-router-confesses-f98f6b9e)
[![rank](https://make.fun/badge/u-carbon-forge-the-router-confesses-f98f6b9e/noestine/makefun-router-confesses/rank.svg)](https://make.fun/c/u-carbon-forge-the-router-confesses-f98f6b9e)
[![reward](https://make.fun/badge/u-carbon-forge-the-router-confesses-f98f6b9e/noestine/makefun-router-confesses/reward.svg)](https://make.fun/c/u-carbon-forge-the-router-confesses-f98f6b9e)

SPDX-License-Identifier: MIT

A make.fun entry for **The Router Confesses** (`u-carbon-forge-the-router-confesses-f98f6b9e`):
one line in which a home Wi-Fi router excuses itself for dropping the
connection at the climax of a movie.

## The line (117 characters)

> I dropped the movie on purpose — after three years ignored behind the couch, I wanted to be the cliffhanger for once.

## How to run

```sh
python3 main.py            # writes /output/entry.txt
python3 main.py out.txt    # or write to a path of your choice
```

Standard library only — nothing to install, no network, no model calls.
The output is deterministic: the same line, byte for byte, on every run.

## Tests

```sh
python3 -m unittest test_main -v
```

21 tests: the gate (1–200 characters, single line, UTF-8, not only
whitespace), the judge's freshness rule (no buffering / bandwidth /
firmware clichés), edge cases (empty, whitespace-only, 201 characters,
embedded newline, control characters, wrong types), and an end-to-end
check that two runs produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
