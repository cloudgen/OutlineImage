**file**: docs/requirements/requirement-runtime-prerequisites.md  
**Status**: Active (Version 1.0.0)  
**Area**: runtime  
**Key**: `requirement-runtime-prerequisites`  
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Declare **host and Python runtime prerequisites** required to run VideoJoin successfully. This product does **not** implement a privileged system `prerequisites` installer command; this file is the **documentation and validation SSOT** for what must already be present.

---

## 2. Core Rules (Mandatory)

### 2.1 Scope (honest product mode)

1. **MUST** document all external tools required at runtime.  
2. **MUST NOT** claim the product auto-installs system packages via root/sudo unless a future Active elev + install requirement is added.  
3. **MUST** separate **pip-installable** Python deps from **system binaries**.

### 2.2 Required runtime components

| Component | Kind | Required for | Install surface |
|-----------|------|--------------|-----------------|
| CPython | interpreter | package import + CLI | OS / pyenv / system Python |
| `ChronicleLogger` | pip package | declared logging dependency | `pyproject.toml` / pip |
| **FFmpeg** (`ffmpeg` on PATH) | system binary | stream-copy concat + re-encode fallback | OS package manager / user install |

### 2.3 Validation expectations

4. **MUST** fail with an actionable message when `ffmpeg` is missing (not a cryptic stack only).  
5. **MUST** document that FFmpeg is **not** installed by `pip install VideoJoin` alone.  
6. **MUST** document first-class input formats as the domain format set (currently multi-extension local video files).

### 2.4 Privilege

7. **MUST NOT** require root to satisfy runtime prerequisites for normal use.  
8. Type 1 elevation for package install is **out of scope** for this product.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Python package install** | `pip install -e .` (primary); wheel/`pip install .` when packaging; PyPI only when actually published |
| **Declared pip deps** | `ChronicleLogger>=1.2.3` (optional for current interactive console paths) |
| **System binary** | `ffmpeg` on `PATH` (**required**) |
| **Auto install command** | **none** (does not install OS FFmpeg) |
| **Platform notes** | Linux primary; macOS/Windows OK when FFmpeg + CPython available |
| **Product version** | 1.0.3 |
| **Startup check** | `ensure_ffmpeg()` in `main()` — `shutil.which` + `ffmpeg -version` |
| **User docs** | Root `README.md` Quick Installation must state FFmpeg is a **system** prerequisite |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Assume FFmpeg may be missing.  
- **Principle 10 – Least privilege**: No root prerequisites command forced.  
- **Principle 2 – Intentional**: External vs pip deps separated.

---

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Document before fail.  
- **Intentional:** No fake “one command installs OS FFmpeg” claim.  
- **Anti-fragile:** Works wherever PATH FFmpeg exists.  
- **Over-protect:** No silent elev install.

---

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Claim FFmpeg is installed by `pip install VideoJoin` alone.  
2. Add root package-manager elev without elev allowlist law and user order.  
3. Drop FFmpeg from prerequisite tables while code still depends on it.  
4. Store secrets in this file.  
5. Invent OpenCV or other unused heavy deps as required without code/law alignment.

**Violating this rule is a critical honesty regression.**

---

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | FFmpeg listed as system binary |
| AC-2 | ChronicleLogger listed as pip dep (as currently required) |
| AC-3 | No false auto root-install claim |
| AC-4 | README aligns with this table |
| AC-5 | Missing FFmpeg produces actionable user message |

---

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|--------------|
| `requirement-python-packaging` | pip deps |
| `requirement-video-ffmpeg-pipeline` | uses FFmpeg |
| `requirement-python-error-handling` | missing tool messages |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-PRE-01** | `tests/test_prerequisites.py` | todo | Host `ffmpeg` or actionable miss |
| **TP-PRE-02** | `tests/test_prerequisites.py` | todo | Import declared pip deps |
| **TP-ERR-01** | `tests/test_errors.py` | todo | Peer missing FFmpeg path |

**Matrix:** `docs/reviews/requirement-test-matrix.md`  
**Map:** `docs/reviews/test-plan.md`


## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial runtime prerequisites law for VideoJoin |

---

**Last Updated**: 2026-08-09  
**Owner**: project maintainers  
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
