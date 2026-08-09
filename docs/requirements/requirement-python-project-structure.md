**file**: docs/requirements/requirement-python-project-structure.md  
**Status**: Active (Version 1.0.0)  
**Area**: python  
**Key**: `requirement-python-project-structure`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the **repository layout** and package structure for VideoJoin as a Python package project: where source, packaging, and requirements law live.

---

## 2. Core Rules (Mandatory)

### 2.1 Source package layout

1. **MUST** keep the installable package under **`src/VideoJoin/`**.  
2. **MUST** include `__init__.py` (version export), `__main__.py` (module entry), and `cli.py` (CLI + domain session).  
3. **MUST NOT** scatter a second installable package name that contradicts packaging SSOT without an explicit rename plan.

### 2.2 Project root layout

4. **MUST** keep `pyproject.toml` at repository root.  
5. **MUST** keep product user docs at root **`README.md`**.  
6. **MUST** keep specialized product law under **`docs/requirements/`** with `requirement-` prefix and registry `index.md`.  
7. Product design notes **MAY** live under `docs/` (e.g. design specs, changelog) without becoming requirement law unless registered.

### 2.3 Generated / non-source

8. **MUST NOT** commit `build/` or `dist/` artifacts as product source of truth.  
9. Egg-info / `__pycache__` / compiled `.so` **MUST** remain ignore-friendly (gitignore).  
10. Optional Cython/`build.sh` tooling **MAY** exist as maintainer tooling; it **MUST NOT** replace `src/VideoJoin` as runtime package SSOT.

### 2.4 Requirements surface discipline

11. All product-law files **MUST** use basename prefix `requirement-`.  
12. **MUST** register every Active requirement in `docs/requirements/index.md`.  
13. Product source comments that cite law **MUST** cite live `requirement-*.md` keys only — never templates or skills as behavioral authority.

### 2.5 Implementation Notes (this project)

| Path | Role |
|------|------|
| `src/VideoJoin/` | Installable package |
| `src/VideoJoin/cli.py` | Interactive CLI + FFmpeg join helpers |
| `src/VideoJoin/__init__.py` | `__version__` |
| `src/VideoJoin/__main__.py` | Module entry |
| `pyproject.toml` | Packaging SSOT |
| `build.sh` | Maintainer build helper |
| `docs/requirements/` | Product law |
| `docs/CHANGELOG.md` | Product changelog (may also use root CHANGELOG.md) |
| `docs/VideoJoin-spec.md` | Design notes (not substitute for requirements) |
| `docs/folder-structure.md` | Layout notes (not substitute for requirements) |
| `tests/` | Planned/executable suites (proof; not law) |
| `README.md` | User documentation (identity triad SSOT) |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Layout is explicit.  
- **Principle 5 – SSOT**: One package path, one requirements registry.  
- **Principle 17 – Storage**: Generated dirs not confused with source.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not invent parallel packages.  
- **Intentional:** `src/` layout for packaging.  
- **Anti-fragile:** Clear ignore of build debris.  
- **Over-protect:** Requirements registry discipline.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Move the installable package out of `src/VideoJoin/` without packaging update.  
2. Delete `docs/requirements/index.md` discipline.  
3. Commit secrets under `src/` or `docs/requirements/`.  
4. Cite templates/skills from product source as product law.  
5. Treat design notes under `docs/*.md` as a second competing law SSOT over Active requirements.

**Violating this rule is a critical structure regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | Package lives under `src/VideoJoin/` |
| AC-2 | Root `pyproject.toml` present |
| AC-3 | Requirements under `docs/requirements/` with index |
| AC-4 | Generated build/dist not source SSOT |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | Manifest |
| `requirement-python-cli-interface` | Entry module |
| `requirement-class-software-dev` | Class residual |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-STRUCT-01** | `tests/test_structure.py` | todo | `src/VideoJoin` layout present |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial project structure law for VideoJoin |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
