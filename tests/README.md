# Tests — VideoJoin

Executable proof for product law. **Design map:** `docs/reviews/test-plan.md`.  
**RTM:** `docs/reviews/requirement-test-matrix.md`.

## Status (2026-08-09, product 1.0.3)

| Item | State |
|------|--------|
| Design TP map | **present** under `docs/reviews/test-plan.md` |
| Automated suites | **not yet implemented** (all Core TP rows `todo`) |
| Runner | planned: `pytest` or `python -m unittest` |

## Planned layout

| File | TP families |
|------|-------------|
| `test_structure.py` | TP-STRUCT |
| `test_packaging.py` | TP-PKG |
| `test_prerequisites.py` | TP-PRE |
| `test_cli.py` | TP-CLI |
| `test_domain_join.py` | TP-VIDEOJOIN |
| `test_ffmpeg_pipeline.py` | TP-FFMPEG |
| `test_errors.py` | TP-ERR |
| `test_fs_publish.py` | TP-FS |

## Rules

1. Assert messages / test names **MUST** include the **TP-ID**.  
2. Run media cases only with **generated fixtures** in temp dirs — never user media.  
3. Core cases **MUST NOT** require public network.  
4. Flip `todo` → `have` in `docs/reviews/test-plan.md` and requirement DTV only after green runs.  
5. Do not place executable tests under `docs/templates/`.

## Run (when suites exist)

```bash
# example once pytest is adopted
pytest -q tests/
```
