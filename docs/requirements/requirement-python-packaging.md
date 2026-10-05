**file**: docs/requirements/requirement-python-packaging.md
**Status**: Active (Version 1.2.2)
**Area**: python
**Key**: `requirement-python-packaging`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the packaging SSOT for the VideoJoin Python distribution: `pyproject.toml`, metadata, dependencies, console entry points, and version consistency.

This file owns the ChronicleLogger floor together with `requirement-runtime-prerequisites`. There is no separate dependency-management requirement.

### 1.1 Human-facing

**In one sentence:** VideoJoin is a pip package named VideoJoin, version 1.0.5, and the status library is a required dependency.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person installing the package | `python -m pip install VideoJoin` |
| The other role | The manifest | `pyproject.toml` names the version, the console script, and the dependencies |
| Not this file | What the menu does after install, and how FFmpeg concatenates | CLI, TUI, and pipeline requirements |

| Includes | Excludes |
|----------|----------|
| Package name, version, console script `video-join`, required `ChronicleLogger>=1.3.1` | Re-exporting ChronicleLogger from the VideoJoin package |
| Manifest floor `ChronicleLogger>=1.3.1`, same as this law | Calling the logger optional, or leaving the manifest at `>=1.2.3` |
| MIT license, homepage, Python range as declared | A claim that pip installs FFmpeg |

| Surface | What you open | What for |
|---------|---------------|----------|
| `pyproject.toml` | `[project]` | Name, version, dependencies, console script |
| `src/VideoJoin/__init__.py` | `__version__` | The same version string |
| pip | Install | `python -m pip install VideoJoin` |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install | pip installs VideoJoin and the required status library. It does not install FFmpeg. | `python -m pip install VideoJoin` |
| Check the version | The badge, the manifest, and `__version__` are the same string. | Open `pyproject.toml` and `__init__.py` |
| Import the package | You get `__version__` and `main`. You do not get ChronicleLogger from this package. | `python -c "import VideoJoin"` |

## 2. Core Rules (Mandatory)

### 2.1 Manifest SSOT

1. `pyproject.toml` **MUST** be the primary packaging manifest (PEP 517 / PEP 621).
2. **MUST** declare: name, version, description, authors, license text, requires-python, dependencies, build-system, and console scripts.
3. **MUST NOT** treat an ad-hoc `requirements.txt` as the primary product dependency SSOT.
4. A legacy `setup.py` under a build tree **MUST NOT** become a second source of runtime identity.

### 2.2 Version SSOT

5. The package version in `pyproject.toml` and `src/VideoJoin/__init__.py` (`__version__`) **MUST** match when a release is claimed.
6. Bumping either **MUST** update both in the same change.
7. **MUST NOT** invent a third version constant. Display code **MUST NOT** keep a second literal, including a fallback `"1.0.5"` (`requirement-python-oop`). The current release string is `1.0.5`. A version bump is a user order, not a side effect of editing this file.

### 2.3 Dependencies

8. **MUST** declare runtime Python dependencies required for the shipped CLI.
9. ChronicleLogger **MUST** be a required dependency at floor `ChronicleLogger>=1.3.1`. It **MUST NOT** be marked optional. The live `pyproject.toml` declares that floor.
10. System tools (FFmpeg) **MUST NOT** be declared as pip packages. Document them under `requirement-runtime-prerequisites`.
11. **MUST NOT** commit secrets or private index passwords into packaging files.
12. **MUST NOT** re-export `ChronicleLogger` from the VideoJoin package.

### 2.4 Entry points

13. **MUST** declare console script `video-join` → `VideoJoin.cli:main`.
14. The entry function **MUST** stay `def main` in `src/VideoJoin/cli.py`. In the allowed end state, `main` constructs ChronicleLogger and then `Cli` (`requirement-python-cli-logging`, `requirement-python-oop`).

### 2.5 Build / release helpers

15. Optional `build.sh` / Cython tooling **MAY** exist for maintainer packaging.
16. **MUST** keep helper scripts consistent with `pyproject.toml` identity (project name VideoJoin).
17. Generated `build/` and `dist/` **MUST NOT** be treated as source SSOT.

### 2.6 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Manifest** | `pyproject.toml` |
| **Project name** | `VideoJoin` |
| **Version** | `1.0.5` |
| **requires-python** | `>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*` (as declared — re-verify support claims before marketing) |
| **Dependencies (law)** | `ChronicleLogger>=1.3.1`, required |
| **Dependencies (live manifest)** | `ChronicleLogger>=1.3.1`. Matches the law floor |
| **Build backend** | `setuptools.build_meta` |
| **Console script** | `video-join = VideoJoin.cli:main` |
| **Homepage / repo** | `https://github.com/Wilgat/VideoJoin` |
| **Maintainer build helper** | `build.sh` |
| **License** | MIT |
| **Public package exports** | `__version__`, `main` only. **MUST NOT** re-export `ChronicleLogger` |
| **User docs** | Root `README.md` Quick Installation documents pip and **MUST NOT** claim pip installs FFmpeg. This pass does not edit that README |
| **README version badge** | Must match packaging version when README claims complete (`1.0.5`) |

### 2.7 Why This Requirement Exists (CIAO)

- **Principle 5 – SSOT**: One manifest for identity and entry. One floor for ChronicleLogger.
- **Principle 2 – Intentional**: The live manifest lag is written down instead of being described as optional.
- **Principle 1 – Caution**: System FFmpeg is not declared as a pip package.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, install and upgrade use pip as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to install VideoJoin. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`. The install line is `python -m pip install VideoJoin`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** The version string has one home in the manifest and one matching `__version__`.
- **Intentional:** PEP 621 is the manifest. The logger floor is required.
- **Anti-fragile:** The console script and the module entry share `main`.
- **Over-protect:** No secrets in packaging files. No re-export of ChronicleLogger.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Remove or rename the `video-join` entry without a CLI and README update.
2. Let `__version__` and `pyproject.toml` diverge while claiming a release.
3. Add private credentials to `pyproject.toml`.
4. Replace the packaging SSOT with only `requirements.txt`.
5. Change the product name silently.
6. Mark ChronicleLogger optional, or leave the manifest at `>=1.2.3` once the packaging file is edited for the floor.
7. Re-export ChronicleLogger from the package.
8. Bump the product version as a side effect of editing this requirement.

**Violating this rule is a critical packaging regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `pyproject.toml` names VideoJoin |
| AC-2 | Console script `video-join` is declared |
| AC-3 | Law and the live manifest both require `ChronicleLogger>=1.3.1` |
| AC-4 | Version matches `__init__.py` when a release is claimed (`1.0.5`) |
| AC-5 | FFmpeg is external, not a pip dependency |
| AC-6 | Public exports are `__version__` and `main` only |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-project-structure` | Package path |
| `requirement-python-cli-interface` | Entry behavior |
| `requirement-python-cli-logging` | Points here for the floor |
| `requirement-runtime-prerequisites` | Same floor. FFmpeg is a system binary |
| `requirement-python-oop` | `main` stays the console target |
| `requirement-class-software-dev` | Residual stack |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PKG-01** | `tests/test_packaging.py` | todo | Console script resolves. Package does not re-export ChronicleLogger |
| **TP-PKG-02** | `tests/test_packaging.py` | todo | `pyproject.toml` version equals `__version__` |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | Peer: ChronicleLogger import. Floor target is `>=1.3.1` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial packaging law for VideoJoin |
| 2026-08-09 | Active 1.1.0 | Export honesty and version 1.0.3 |
| 2026-10-04 | Active 1.2.0 | ChronicleLogger is required at `>=1.3.1`. Live manifest still `>=1.2.3`. Product version stays 1.0.3 |
| 2026-10-04 | Active 1.2.1 | Product version **1.0.4**. Manifest floor is `ChronicleLogger>=1.3.1` |
| 2026-10-04 | Active 1.2.2 | Product version **1.0.5**. Floor stays `ChronicleLogger>=1.3.1` |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
