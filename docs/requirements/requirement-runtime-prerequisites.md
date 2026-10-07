**file**: docs/requirements/requirement-runtime-prerequisites.md
**Status**: Active (Version 1.2.2)
**Area**: runtime
**Key**: `requirement-runtime-prerequisites`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare the host and Python runtime prerequisites required to run OutlineImage. This product does not implement a privileged installer. This file is the documentation and validation SSOT for what must already be present. The pip strings are `requirement-python-dependency-management`.

### 1.1 Human-facing

**In one sentence:** You need Python, ChronicleLogger, and the image stack. No encoder is required.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person about to outline a folder | Pip already installed the image stack |
| The other role | pip | Installs OutlineImage, ChronicleLogger, Pillow, numpy, opencv-python-headless, and rembg |
| Not this file | The menu picture and the outline steps | TUI and the domain file |

| Includes | Excludes |
|----------|----------|
| The image stack as pip packages | A claim that a host `ffmpeg` binary is required |
| ChronicleLogger `>=1.3.1`, required | Calling that library optional |
| A console next step when a required import is missing | Root auto-install |

| Surface | What you open | What for |
|---------|---------------|----------|
| pip | ChronicleLogger, Pillow, numpy, opencv-python-headless, rembg | Status file and outline images |
| About page | Runtime-tools line | The word `none`. Does not probe PATH (`requirement-python-about`) |
| First outline that has an image | Model `isnet-general-use` | May download that model. An empty folder does not |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Install the Python package | You get OutlineImage, the status library, and the image stack. | `python -m pip install OutlineImage` |
| Convert an empty folder | The program returns 0 and does not load the model. | `outline-image outline` |
| Start with the logger library missing | The console prints the pip next step and returns non-zero. | `outline-image` |

## 2. Core Rules (Mandatory)

### 2.1 Scope

1. **MUST** document every external tool required at runtime.
2. **MUST NOT** claim the product auto-installs system packages via root or sudo.
3. **MUST** separate pip-installable Python dependencies from system binaries.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython `>=3.10` | interpreter | package import and the CLI | OS, pyenv, or the system Python. This product does not require you to install pyenv |
| ChronicleLogger `>=1.3.1` | pip package | the one status logger | `requirement-python-dependency-management`. Required, not optional |
| `numpy>=2.3.0`, `Pillow>=12.1.0`, `opencv-python-headless>=5.0.0.93`, `rembg>=2.0.85` | pip packages | an outline when the folder has a supported image | `requirement-python-dependency-management`. Required. An empty folder does not import them |
| FFmpeg | not required | nothing in this product | not installed and not checked |

### 2.3 Validation

4. **MUST NOT** fail because `ffmpeg` is missing. The front board and `outline` do not look for it.
5. The front board **MAY** open when the image stack is not imported yet. About does not probe those packages and does not install them.
6. **MUST** document that FFmpeg is not installed by `pip install OutlineImage` and is not required.
7. **MUST** document the input formats as the domain format set.
8. If `ChronicleLogger` cannot be imported, `def main` **MUST** print the pip next step and return non-zero (`requirement-python-cli-logging`). That line is console text. The library is required. If the image stack cannot be imported while a folder has a supported image, `outline` **MUST** print the pip next step and return 1.

### 2.4 Privilege

9. **MUST NOT** require root to satisfy runtime prerequisites for normal use.
10. Type 1 elevation is out of scope.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `python -m pip install OutlineImage`, or `python -m pip install -e .` from a checkout |
| **Declared pip dependency (law)** | The five strings in `requirement-python-dependency-management`. All required |
| **Live manifest** | `pyproject.toml` lists those five strings. `requires-python` is `>=3.10` |
| **System binary** | none. `ffmpeg` is not required |
| **Auto install command** | none. The product does not run a root install. The first outline that has an image may download model `isnet-general-use` |
| **Platform notes** | Linux primary. macOS and Windows when CPython is available |
| **Product version** | 1.0.1 |
| **Startup check** | No encoder check. The image stack is imported only when the chosen folder has a supported image |
| **User docs** | Root `README.md` names the pip image stack and says no external media tool is required |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: A missing image library is reported when an image is actually converted.
- **Principle 10 – Least privilege**: No root installer.
- **Principle 2 – Intentional**: The pip libraries and a host encoder are different facts. This product has no host encoder.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the normal user installs the pip package. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to install ChronicleLogger or the image stack from inside OutlineImage. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document a missing library before the conversion claims success.
- **Intentional:** pip installs the image stack. It does not install FFmpeg. ChronicleLogger is required.
- **Anti-fragile:** An empty folder still returns 0 without the model.
- **Over-protect:** No silent root install.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Claim FFmpeg is installed by `pip install OutlineImage`, or claim this product requires it.
2. Add a root package-manager install from this product.
3. Treat a missing `ffmpeg` binary as a failed outline.
4. Store secrets in this file.
5. Drop Pillow, numpy, opencv-python-headless, or rembg while `outline` still imports them for a folder that has an image.
6. Call ChronicleLogger optional.

**Violating this rule is a critical honesty regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | FFmpeg is listed as not required |
| AC-2 | ChronicleLogger is required at `>=1.3.1`, and the image floors are `requirement-python-dependency-management` |
| AC-3 | No root auto-install claim |
| AC-4 | A missing image library on a folder that has an image produces the pip next step |
| AC-5 | Missing ChronicleLogger produces the pip next step and a non-zero return |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-dependency-management` | Pip strings |
| `requirement-python-packaging` | Manifest shape |
| `requirement-python-cli-logging` | Construct. Missing-import sentence |
| `requirement-video-ffmpeg-pipeline` | Retired. This file does not require an encoder |
| `requirement-python-error-handling` | Missing-library messages |
| `requirement-domain-outlineimage` | About runtime-tools line is `none` |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PRE-01** | `tests/test_outline.py` | have | An empty folder does not import the image stack |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | ChronicleLogger imports. Law floor is `>=1.3.1` |
| **TP-ERR-01** | `tests/test_outline.py` | have | A missing folder returns 1. An empty folder returns 0 |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law for OutlineImage |
| 2026-10-04 | Active 1.1.0 | ChronicleLogger `>=1.3.1` is required. Live manifest still `>=1.2.3`. FFmpeg stays a system binary. The front board may open without it |
| 2026-10-04 | Active 1.1.1 | Product version **1.0.4**. Manifest floor is `ChronicleLogger>=1.3.1` |
| 2026-10-04 | Active 1.1.2 | The about page names FFmpeg and does not probe PATH. Product version **1.0.5** |
| 2026-10-05 | Active 1.2.0 | No host encoder. Image stack is pip. Product version **1.0.0**. About runtime tools are `none` |
| 2026-10-05 | Active 1.2.1 | Pip strings point at `requirement-python-dependency-management`. Product version stays **1.0.0** |
| 2026-10-07 | Active 1.2.2 | Product version is **1.0.1** |

---

**Last Updated**: 2026-10-07
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
