**file**: docs/requirements/requirement-python-error-handling.md
**Status**: Active (Version 1.2.0)
**Area**: python
**Key**: `requirement-python-error-handling`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define how OutlineImage detects, reports, and recovers from errors during the text menu and the `outline` verb without destroying the source images.

Console sentences in this file stay required. Durable status, once the logger exists, is `requirement-python-cli-logging`. ChronicleLogger is required. It is not optional.

### 1.1 Human-facing

**In one sentence:** When an outline cannot be written, OutlineImage tells you why and leaves the source image where it is.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person whose folder is missing or whose image failed | You see the reason and can try again or stop |
| The other role | The status file | The same fact is written by ChronicleLogger after `main` has constructed it |
| Not this file | The menu frame, and the outline steps | `requirement-python-tui`, `requirement-domain-outlineimage` |

| Includes | Excludes |
|----------|----------|
| A readable failure sentence. Source images left intact | A silent success after an image failed |
| Continue with the next image after one failure | Stopping the whole folder on the first failure without saying which file failed |
| The missing-library sentence, printed before any logger exists | Sending that one line through `log_message` |

| Surface | What you open | What for |
|---------|---------------|----------|
| Outline result | The terminal, or the menu result page | The reason |
| `outline-image outline` on a missing folder | Message, exit 1 | Nothing is written |
| Console before the logger exists | Missing ChronicleLogger | The pip next step |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Name a folder that is not there | Exit 1. The next step names `outline-image outline`. | `outline-image outline missing` |
| Convert a folder with no supported image | Exit 0. The model is not loaded. | `outline-image outline` |
| Run without the logger library | The console names the pip next step and the program returns non-zero. | `outline-image` |

## 2. Core Rules (Mandatory)

### 2.1 Fail-closed principles

1. **MUST NOT** silently ignore a failed image when the product claims success.
2. **MUST NOT** treat a missing folder or a bad format as success.
3. **MUST** prefer clear human-readable messages over stack traces for expected user mistakes.
4. **MUST** leave every source image intact on all failure paths.

### 2.2 Required error categories

| Category | Detection | Required action |
|----------|-----------|-----------------|
| Folder is not a directory | `Path.is_dir()` is false | Message. Exit 1. Next step `outline-image outline` |
| Unsupported format | extension not in the domain set | Message. Exit 1. Next step names `--format png` |
| No supported image | the folder exists and the top-level set is empty | Message. Exit 0. Do not import the image stack |
| Image library missing | import fails while the folder has an image | Message naming Pillow, opencv-python-headless, numpy, and rembg. Exit 1. Next step is pip install |
| Model will not load | `new_session` fails | Message. Exit 1 |
| One image fails | exception from that file | Report that file. Continue with the rest. Exit 1 if any file failed |
| Output directory cannot be created | `mkdir` raises | Message. Exit 1. Do not convert |
| ChronicleLogger missing | import fails inside `def main` | Console next step from `requirement-python-cli-logging`. Return non-zero. That line cannot use `log_message` |
| Empty argv with no terminal | stdout is not a terminal | Help text. Return 0. This is not a failure |
| Unknown verb, including `hello`, `join`, and `list-videos` | not in `PRODUCT_VERBS` | Message. Exit non-zero |

### 2.3 Sources stay

5. **MUST NOT** delete a source image as cleanup.
6. **MUST NOT** delete an outline that was already written for an earlier image in the same run.
7. A missing `ffmpeg` binary is not an error. Do not report it.
8. The output directory is `<folder>/output` unless the caller passed another directory.

### 2.4 Logging and the console

9. Once `def main` has constructed ChronicleLogger, durable status **MUST** go through that logger. The logger is required (`requirement-python-packaging`).
10. **MUST** still show the user-visible failure reason. On the text screen it sits in the menu region. Off the text screen it is a console line. A quiet logger mirror is not a substitute for that sentence.
11. **MUST NOT** log secrets. This product has none.
12. **MUST NOT** hang on `input()` when stdout is not a terminal.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Missing folder** | Exit 1. Next step `outline-image outline` |
| **Empty folder** | Exit 0. The image stack is not imported |
| **One failed image** | That file is named. Later files still run. Exit 1 |
| **Image library** | Exit 1 and the pip next step, only when the folder has a supported image |
| **ChronicleLogger** | Required. Missing import is a console sentence and a non-zero return, before any `log_message` |
| **No terminal** | Empty argv prints help and returns 0. `outline` still converts |
| **Encoder** | Not checked |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 1 – Caution**: Fail closed on a missing folder and on a failed image.
- **Principle 11 – Sources**: Do not delete the picture that was converted.
- **Principle 12 – Traceability**: The operator still sees the failure when the log mirror is quiet.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, failure sentences are for the normal user who started `outline-image`. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to report an error or to clean a temp. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An empty folder never loads the model.
- **Intentional:** The category table is the failure contract.
- **Anti-fragile:** One failed image does not hide the others.
- **Over-protect:** Source images stay in place.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Swallow an image error without a user-visible failure.
2. Delete a source image on error.
3. Claim success after a failed image.
4. Replace clear messages with a silent pass.
5. Log credentials or tokens.
6. Call the logger optional, or send the missing-library line through `log_message`.
7. Hang on a prompt when there is no terminal.

**Violating this rule is a critical safety regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | A missing folder returns 1 |
| AC-2 | An empty folder returns 0 and does not import the image stack |
| AC-3 | Source images remain after failure |
| AC-4 | One failed image is named and does not skip the report |
| AC-5 | A bad format returns 1 |
| AC-6 | A failed image does not present the run as success |
| AC-7 | Missing ChronicleLogger is a console next step and a non-zero return |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-video-ffmpeg-pipeline` | Retired. A missing encoder is not a failure |
| `requirement-python-cli-interface` | Verb exits |
| `requirement-python-tui` | Where the sentence sits on the screen |
| `requirement-python-cli-logging` | Durable status after the construct |
| `requirement-runtime-prerequisites` | Missing image library and the logger floor |
| `requirement-domain-outlineimage` | Session outcomes |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-ERR-01** | `tests/test_outline.py` | have | A missing folder returns 1 |
| **TP-ERR-02** | `tests/test_outline.py` | have | An empty directory returns 0 and does not import the image stack |
| **TP-ERR-03** | `tests/test_outline.py` | have | The empty-folder message names the directory |
| **TP-LOG-01** | `tests/test_logging.py` | todo | Peer: missing library is a console line, not `log_message` |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial error-handling law for OutlineImage |
| 2026-08-09 | Active 1.1.0 | Fail-closed fallback and unique temp cleanup notes |
| 2026-10-04 | Active 1.2.0 | ChronicleLogger is required for durable status. Console sentences stay. Missing library is a console line. Empty argv off a terminal is help, return 0 |

---

**Last Updated**: 2026-10-04
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
