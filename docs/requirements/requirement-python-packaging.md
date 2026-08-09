**file**: docs/requirements/requirement-python-packaging.md  
**Status**: Active (Version 1.1.0)  
**Area**: python  
**Key**: `requirement-python-packaging`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define packaging SSOT for the VideoJoin Python distribution: **`pyproject.toml`**, metadata, dependencies, console entry points, and version consistency.

---

## 2. Core Rules (Mandatory)

### 2.1 Manifest SSOT

1. **`pyproject.toml` MUST** be the primary packaging manifest (PEP 517 / PEP 621).  
2. **MUST** declare: name, version, description, authors, license text, requires-python, dependencies, build-system, and console scripts.  
3. **MUST NOT** treat an ad-hoc `requirements.txt` as the primary product dependency SSOT.  
4. Legacy `setup.py` under build trees **MUST NOT** become a second source of runtime identity without deprecation plan.

### 2.2 Version SSOT

5. Package version in **`pyproject.toml`** and **`src/VideoJoin/__init__.__version__`** **MUST** match when a release is claimed.  
6. Bumping either **MUST** update both in the same change (or automated single writer documented later).  
7. **MUST NOT** invent a third silent version constant without declaring the new SSOT.

### 2.3 Dependencies

8. **MUST** declare runtime Python dependencies required for the shipped CLI.  
9. System tools (FFmpeg) **MUST NOT** be faked as pip packages — document under runtime prerequisites.  
10. **MUST NOT** commit real secrets or private index passwords into packaging files.

### 2.4 Entry points

11. **MUST** declare console script **`video-join`** → `VideoJoin.cli:main`.  
12. Entry function **MUST** remain a thin launch into product logic (interactive session today).

### 2.5 Build / release helpers

13. Optional `build.sh` / Cython tooling **MAY** exist for maintainer packaging.  
14. **MUST** keep helper scripts consistent with `pyproject.toml` identity (project name VideoJoin).  
15. Generated `build/` and `dist/` **MUST NOT** be treated as source SSOT.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Manifest** | `pyproject.toml` |
| **Project name** | `VideoJoin` |
| **Version** | `1.0.3` |
| **requires-python** | `>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*` (as declared — re-verify support claims before marketing) |
| **Dependencies** | `ChronicleLogger>=1.2.3` (optional at runtime for current CLI; declared for ecosystem compatibility) |
| **Build backend** | `setuptools.build_meta` |
| **Console script** | `video-join = VideoJoin.cli:main` |
| **Homepage / repo** | `https://github.com/Wilgat/VideoJoin` |
| **Maintainer build helper** | `build.sh` |
| **License** | MIT (packaging claims MIT; ensure root LICENSE file present when publishing) |
| **Public package exports** | `__version__`, `main` only — **MUST NOT** re-export undefined `ChronicleLogger` from `.cli` |
| **User docs** | Root `README.md` Quick Installation must document local `pip install -e .`, console script `video-join`, and **not** claim a live PyPI release unless published |
| **README version badge** | Must match packaging version when README claims complete (**1.0.3**) |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest for identity and entry.  
- **Principle 2 – Intentional**: Version dual-write is explicit.  
- **Principle 1 – Caution**: System FFmpeg not mis-declared as pip-only.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Validate version dual SSOT on release.  
- **Intentional:** PEP 621 over ad-hoc manifests.  
- **Anti-fragile:** Console script + module entry.  
- **Over-protect:** No secrets in packaging files.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Remove or rename `video-join` entry without CLI + README update.  
2. Let `__version__` and `pyproject.toml` diverge while claiming a release.  
3. Add private credentials to `pyproject.toml`.  
4. Replace packaging SSOT with only `requirements.txt`.  
5. Change product name silently across packaging and source package directory.

**Violating this rule is a critical packaging regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `pyproject.toml` present with name VideoJoin |
| AC-2 | Console script `video-join` declared |
| AC-3 | Dependencies include ChronicleLogger (as currently required) |
| AC-4 | Version matches `__init__.py` when release claimed |
| AC-5 | FFmpeg documented as external, not pip-only |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-project-structure` | Package path |
| `requirement-python-cli-interface` | Entry behavior |
| `requirement-runtime-prerequisites` | External tools |
| `requirement-class-software-dev` | Residual stack |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PKG-01** | `tests/test_packaging.py` | todo | Entry imports / console script |
| **TP-PKG-02** | `tests/test_packaging.py` | todo | version dual SSOT |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial packaging law for VideoJoin |
| 2026-08-09 | Active 1.1.0 | Export honesty + version 1.0.3 |
| 2026-08-09 | Active 1.1.0 | README install honesty notes (local primary; no false PyPI) |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
