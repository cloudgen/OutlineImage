# Requirements

Authoritative specialized product law for **OutlineImage** lives here.

**Current state (2026-10-05):** Specialized **software-development** product. Left genesis. Registry is populated — see `index.md`. Fifteen Active requirements and one Retired encoder file. Product version is **1.0.0**.

## Product identity (summary)

| Field | Value |
|-------|--------|
| Product / package | `OutlineImage` |
| Version SSOT | **`1.0.0`** (`pyproject.toml` + `src/OutlineImage/__init__.py`) |
| Product README SSOT | Root `README.md` (app-name, short description, target version **1.0.0**). Sections and pictures: `requirement-python-readme` |
| Ship surface | Python package; console script **`outline-image`**; module `python -m OutlineImage`; checkout entry `./convert.py` |
| Install mode | **pip / local package** (`pip install OutlineImage`; this tree **1.0.0**; checkout `pip install -e .`) — not shell Type O |
| Domain surface | `requirement-domain-outlineimage` — four pillars (`outline`, the folder board, help, about) |
| Text menu | `requirement-python-tui` — front rows outline, system-log, language, self-management, Exit. Row 1 lists the current folder, each subfolder, and back. Default path word is `Path` |
| Menu language | `requirement-python-cli-language` — row 4, thirteen codes, leaf `~/.local/OutlineImage/language`. `language` is not an argv verb |
| Status logger | `requirement-python-cli-logging` — `ChronicleLogger(...)` inside `def main`. Required |
| Class map | `requirement-python-oop` — allowed end state. Running tree is still three modules |
| Encode ops | `requirement-video-ffmpeg-pipeline` — **Retired**. No encoder and no media publish |
| Coding style | `requirement-python-coding-style` — temps + `shutil.move` when a publish-from-temp exists; gate **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** |
| Runtime tools | No host binary. Pip strings are `requirement-python-dependency-management`: **ChronicleLogger>=1.3.1**, **numpy>=2.3.0**, **Pillow>=12.1.0**, **opencv-python-headless>=5.0.0.93**, **rembg>=2.0.85** |

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
5. Sole domain SSOT: `requirement-domain-outlineimage.md`.  
6. When changing outline output: update the domain file **and** root `README.md` in the same change.  
7. Version dual SSOT + README Version badge must match when a release is claimed.
