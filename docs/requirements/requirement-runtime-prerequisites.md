**file**: docs/requirements/requirement-runtime-prerequisites.md
**Status**: Active (Version 1.1.2)
**Area**: runtime
**Key**: `requirement-runtime-prerequisites`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare the host and Python runtime prerequisites required to run VideoJoin. This product does not implement a privileged installer. This file is the documentation and validation SSOT for what must already be present, together with the ChronicleLogger floor also owned by `requirement-python-packaging`.

### 1.1 Human-facing

**In one sentence:** You need Python, the ChronicleLogger package, and FFmpeg on your PATH before a join can finish.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person about to join two videos | FFmpeg is already installed by you, not by pip |
| The other role | pip | Installs VideoJoin and ChronicleLogger. It does not install FFmpeg |
| Not this file | The menu picture and the concat command | TUI and pipeline requirements |

| Includes | Excludes |
|----------|----------|
| FFmpeg on PATH, required for `join` | A claim that `pip install VideoJoin` installs FFmpeg |
| ChronicleLogger `>=1.3.1`, required | Calling that library optional |
| A console next step when either one is missing | Root auto-install of either one |

| Surface | What you open | What for |
|---------|---------------|----------|
| PATH | `ffmpeg` | Concat and the fallback re-encode |
| pip | ChronicleLogger | Status file |
| About page | Runtime-tools line | Names FFmpeg. Does not probe PATH (`requirement-python-about`) |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install the Python package | You get VideoJoin and the status library. | `python -m pip install VideoJoin` |
| Prepare a join | FFmpeg must already be on PATH. The menu may open before that check. | `ffmpeg -version` |
| Start with the library missing | The console prints the pip next step and returns non-zero. | `video-join` |

## 2. Core Rules (Mandatory)

### 2.1 Scope

1. **MUST** document every external tool required at runtime.
2. **MUST NOT** claim the product auto-installs system packages via root or sudo.
3. **MUST** separate pip-installable Python dependencies from system binaries.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython | interpreter | package import and the CLI | OS, pyenv, or the system Python. This product does not require you to install pyenv |
| ChronicleLogger `>=1.3.1` | pip package | the one status logger | `pyproject.toml` / `python -m pip`. Required, not optional |
| FFmpeg (`ffmpeg` on PATH) | system binary | stream-copy concat and the re-encode fallback | the operator’s own install. Not pip |

### 2.3 Validation

4. **MUST** fail with an actionable message when `join` runs and `ffmpeg` is missing.
5. The front board **MAY** open when `ffmpeg` is missing. About reports whether it is on PATH. About does not install it.
6. **MUST** document that FFmpeg is not installed by `pip install VideoJoin`.
7. **MUST** document the input formats as the domain format set.
8. If `ChronicleLogger` cannot be imported, `def main` **MUST** print the pip next step and return non-zero (`requirement-python-cli-logging`). That line is console text. The library is required.

### 2.4 Privilege

9. **MUST NOT** require root to satisfy runtime prerequisites for normal use.
10. Type 1 elevation is out of scope.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `python -m pip install VideoJoin`, or `python -m pip install -e .` from a checkout |
| **Declared pip dependency (law)** | `ChronicleLogger>=1.3.1`, required |
| **Live manifest** | `pyproject.toml` lists `ChronicleLogger>=1.3.1`. Matches the law floor |
| **System binary** | `ffmpeg` on PATH, required for `join` |
| **Auto install command** | none. pip does not install FFmpeg. The product does not run a root install |
| **Platform notes** | Linux primary. macOS and Windows when FFmpeg and CPython are available |
| **Product version** | 1.0.5 |
| **Startup check** | FFmpeg is checked when `join` runs (`shutil.which` and `ffmpeg -version`). It is not a gate on the front board |
| **User docs** | Root `README.md` states FFmpeg is a system prerequisite. This pass does not edit that README |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: FFmpeg may be missing. The join says so.
- **Principle 10 – Least privilege**: No root installer.
- **Principle 2 – Intentional**: The pip library and the system binary are different rows.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the normal user installs the pip package and supplies FFmpeg. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to install ChronicleLogger or FFmpeg from inside VideoJoin. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document the missing tool before the join fails.
- **Intentional:** pip does not install FFmpeg. ChronicleLogger is required.
- **Anti-fragile:** Join works wherever `ffmpeg` is already on PATH.
- **Over-protect:** No silent root install.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Claim FFmpeg is installed by `pip install VideoJoin`.
2. Add a root package-manager install from this product.
3. Drop FFmpeg from the table while `join` still depends on it.
4. Store secrets in this file.
5. Add OpenCV or another unused library as a requirement.
6. Call ChronicleLogger optional, or hide the manifest lag.

**Violating this rule is a critical honesty regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | FFmpeg is listed as a system binary |
| AC-2 | ChronicleLogger is a required pip dependency at `>=1.3.1`. The live manifest lag is stated |
| AC-3 | No root auto-install claim |
| AC-4 | Missing FFmpeg on `join` produces an actionable message |
| AC-5 | Missing ChronicleLogger produces the pip next step and a non-zero return |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-packaging` | Floor owner for the pip dependency |
| `requirement-python-cli-logging` | Construct. Missing-import sentence |
| `requirement-video-ffmpeg-pipeline` | Uses FFmpeg |
| `requirement-python-error-handling` | Missing-tool messages |
| `requirement-domain-videojoin` | About reports FFmpeg |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PRE-01** | `tests/test_prerequisites.py` | todo | Host `ffmpeg`, or an actionable miss on `join` |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | ChronicleLogger imports. Law floor is `>=1.3.1` |
| **TP-ERR-01** | `tests/test_errors.py` | todo | Peer: missing FFmpeg on `join` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law for VideoJoin |
| 2026-10-04 | Active 1.1.0 | ChronicleLogger `>=1.3.1` is required. Live manifest still `>=1.2.3`. FFmpeg stays a system binary. The front board may open without it |
| 2026-10-04 | Active 1.1.1 | Product version **1.0.4**. Manifest floor is `ChronicleLogger>=1.3.1` |
| 2026-10-04 | Active 1.1.2 | The about page names FFmpeg and does not probe PATH. Product version **1.0.5** |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
