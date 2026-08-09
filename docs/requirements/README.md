# Requirements

Authoritative specialized product law for **VideoJoin** lives here.

**Current state (2026-08-09):** Specialized **software-development** product. Left genesis. Registry is populated — see `index.md`.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `VideoJoin` |
| Version SSOT | **`1.0.3`** (`pyproject.toml` + `src/VideoJoin/__init__.py`) |
| Product README SSOT | Root `README.md` (app-name, short description, target version **1.0.3**) |
| Ship surface | Python package; console script **`video-join`**; module `python -m VideoJoin` |
| Install mode | **pip / local package** (`pip install -e .`) — not shell Type O |
| Domain surface | `requirement-domain-videojoin` — four pillars (two-file join) |
| Encode ops | `requirement-video-ffmpeg-pipeline` — stream-copy then re-encode; unique temps; **`shutil.move`** publish |
| Coding style | `requirement-python-coding-style` — temps + `shutil.move`; gate **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** |
| Runtime tools | **FFmpeg** (system binary on PATH); ChronicleLogger optional for current CLI paths |

## Class requirement gate

| Class | Required class file |
|-------|---------------------|
| software-development | `requirement-class-software-dev.md` (**Active**) |
| genesis-template | N/A — this workspace is no longer genesis for product law |

## Purpose

- **Plan** designs work by reading and updating these docs.  
- **Implement** delivers code that **traces** to these requirements.  
- **Review** verifies delivery against requirements and CIAO checklists.  
- Product **README** must stay honest with this law (install, features, version).

## Layout

| Path | Role |
|------|------|
| `docs/requirements/index.md` | Registry of all requirements — keep in sync |
| `docs/requirements/requirement-*.md` | CIAO-style project requirements |

## Status values

Typical: `draft` · `Active` · `approved` · `in-progress` · `done` · `deprecated` · `superseded`

## Rules

1. Never invent paths — verify on disk.  
2. Class files only via class process; non-class via create-specific process.  
3. Never dump harness inventories into this versioned surface.  
4. Online shell install and Type 1 elevation stay **absent** unless product mode is explicitly changed.  
5. Sole domain SSOT: `requirement-domain-videojoin.md`.  
6. When changing join/publish behavior: update pipeline + coding-style REQs **and** root `README.md` in the same change.  
7. Version dual SSOT + README Version badge must match when a release is claimed.
