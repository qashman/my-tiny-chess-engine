# my-tiny-chess-engine

Single-file Python chess agent for make.fun's tiny-chess-01 bounty (stdlib only, Kaggle chess format).

## Status

Updated 2026-11-22. Works, minified to 871 bytes. `main.agent(observation, configuration)` returns one legal move via a 1-ply greedy search. 10 tests pass with `python -m unittest`.

## Run

```sh
python main.py          # import check
python -m unittest -v  # tests
```

## Map

- `main.py` — `apply_move` (module level, pure) and `agent`, which holds `e` (evaluation) and the move loop; `cv` orders captures first. Everything is 1–2 characters except the two names the harness and tests import: `agent` and `apply_move`.
- `test_main.py` — `apply_move_original` is the frozen pre-optimisation version, used as a differential oracle against `main.apply_move`.

## Decisions

- Board index is `(rank - 1) * 8 + file`, so 0 is a1 and 63 is h8. UCI characters are decoded with `ord()` (`ord("1") == 49`, `ord("a") == 97`) rather than `int()`.
- `apply_move` was lifted out of `agent` to module level so tests can import it; it captures nothing from `observation`.
- The evaluator is documented here, not in `main.py`, because comments cost bytes against the bounty's 4,096 cap. In short: `v` is material (black negative, so one pass is white-minus-black), the knight-only `pst` bonus adds a flat +5 when the mirrored entry is positive, and `e` flips sign unless `mark == 1`.
