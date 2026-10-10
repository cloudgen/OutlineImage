**file**: docs/requirements/requirement-python-cli-interface.md
**Status**: Active (Version 1.1.6)
**Area**: python
**Key**: `requirement-python-cli-interface`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

Define the official command-line entry points, empty-argv behavior, and typed verbs for the OutlineImage Python package.

The text-menu picture is `requirement-python-tui`. Outline steps and formats are `requirement-domain-outlineimage`. The about page is `requirement-python-about`. The domain sentence stays on the domain file. The logger construct is `requirement-python-cli-logging`. Class homes are `requirement-python-oop`. The encoder file is Retired.

`def main` writes `ChronicleLogger(...)` and then constructs `Cli`. The argument parser runs after that construct and after the debug block. The allowed end state is this file.

### 1.1 Human-facing

**In one sentence:** `outline-image` with no words opens the numbered menu on a terminal, and with no terminal it prints help and stops.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person at the keyboard or in a script | `outline-image` or `outline-image outline` |
| The other role | The menu picture and the outline facts | `requirement-python-tui`, `requirement-domain-outlineimage` |
| Not this file | How the frame is drawn, and how one image becomes an outline | TUI and the domain file |

| Includes | Excludes |
|----------|----------|
| Console script, module entry, typed verbs, empty-argv menu or help | A shell installer on empty argv |
| `outline`, an optional folder, and `--format`, also owned by the domain file | A numbered row for `help` |
| Pip verbs `version-check`, `self-update`, `self-install`, `self-uninstall`, also owned by the text menu | `sudo` pip, or a downloaded script piped into a shell |

| Surface | What you open | What for |
|---------|---------------|----------|
| `outline-image` on a terminal | Front board | Menu. Does not convert a folder |
| `outline-image` with no terminal | Help text | Exit 0 |
| `outline-image outline` | The terminal | Convert one folder. No menu and no prompt |
| `outline-image help` | Help text | Verb list. Does not draw the menu |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Start on a terminal | The front board opens. Pip does not run. | `outline-image` |
| Start in a script | Help text, exit 0. | `outline-image` |
| Convert a folder | PNG outlines in that folder's `output` directory. No menu. | `outline-image outline` |
| Check or change the install | Pip runs only when you ask. Empty argv does not. | `outline-image version-check` |

## 2. Core Rules (Mandatory)

### 2.1 Entry points

1. **MUST** expose a console script entry named `outline-image` pointing at `OutlineImage.cli:main` (declared in packaging SSOT).
2. **MUST** support module execution: `python -m OutlineImage`.
3. **MUST** keep `def main` in `src/OutlineImage/cli.py` as the single runtime entry. `main` writes `ChronicleLogger(...)` before it constructs `Cli` (`requirement-python-cli-logging`, `requirement-python-oop`).
4. **MUST NOT** require root or sudo to run the CLI.

### 2.2 Empty argv

5. On a terminal, bare invocation (`outline-image` with no args, or `python -m OutlineImage` with no args) **MUST** open the front board in `requirement-python-tui`. It **MUST NOT** convert a folder. It **MUST NOT** run pip.
6. When stdout is not a terminal, bare invocation **MUST** print help and return 0. It **MUST NOT** draw the text screen and **MUST NOT** wait.
7. **MUST NOT** default empty argv to a shell-channel install or to self-update.

### 2.3 Typed verbs

8. `ArgumentParser.parse_args` **MUST** run after `ChronicleLogger(...)` and after the debug block.
9. The typed verbs are `help`, `version`, `about`, `outline`, `self-install`, `version-check`, `self-update`, and `self-uninstall`. Each one is operational. **MUST NOT** add a verb whose only purpose is a test. **MUST NOT** add `hello`, `join`, or `list-videos`. `language` is not a typed verb. Menu row 4 owns it (`requirement-python-cli-language`). **MUST NOT** add `language` to `PRODUCT_VERBS`.
10. A folder operand and `--format` / `-f` are legal only on `outline`. On any other verb they **MUST** be an error. `outline` **MUST NOT** scan subfolders for images.
11. On a terminal, `outline` **MUST NOT** draw the text screen and **MUST NOT** prompt. `about` **MUST** open the about page.
12. With no terminal, `about` **MUST** print the about page and return 0. It does not draw the text screen. `outline` **MUST** convert and return the code from `requirement-domain-outlineimage`. It does not draw the text screen.
13. `help` and `outline` **MUST NOT** draw the text screen. `help` returns 0. `outline` with no folder converts the current directory. The default format is png. Menu row 1 opens the folder board and does not run this verb by itself.
14. `version` **MUST** print `__version__` and **MUST NOT** call pip and **MUST NOT** draw the text screen.
15. `version-check`, `self-update`, `self-install`, and `self-uninstall` **MUST NOT** open the text screen. The commands are:

| Verb | Command |
|------|---------|
| `version-check` | `python -m pip index versions OutlineImage` |
| `self-update` | `python -m pip install --upgrade OutlineImage` |
| `self-install` | `python -m pip install OutlineImage` |
| `self-uninstall` | `python -m pip uninstall -y OutlineImage` only when `--force` is also present |

`self-uninstall` without `--force` **MUST** print the next step and return non-zero. The package stays installed. These commands **MUST NOT** use `sudo` and **MUST NOT** use `curl`. Empty argv **MUST NOT** run `self-install` or `self-update`.

Every typed verb is named again by its topic owner. Help text is not that second mention.

| Verb | Second mention |
|------|----------------|
| `help`, `outline`, `version` | This file for `help`. `outline` is also pillar A of `requirement-domain-outlineimage`. `version` is also row 82 on `requirement-python-tui` |
| `about` | `requirement-python-about` and row 83. The domain sentence stays on pillar D of `requirement-domain-outlineimage` |
| `self-install`, `version-check`, `self-update`, `self-uninstall` | Rows 84–87 on `requirement-python-tui` |

`language` is not in this table. The second mention of that ban is `requirement-python-cli-language`.

Complete invocation samples:

```text
outline-image
outline-image help
outline-image outline
outline-image outline photos --format png
outline-image version
outline-image about
outline-image self-install
outline-image version-check
outline-image self-update
outline-image self-uninstall --force
python -m OutlineImage
```

### 2.4 Outline conversion

These rules are the `outline` verb. The domain file owns the image steps, the folder board, and the output name. They are not what empty argv does.

16. **MUST** accept an optional folder. When it is omitted, the folder is the current directory.
17. **MUST** accept `--format` / `-f` with the domain format set. The default is png.
18. **MUST NOT** prompt. **MUST NOT** draw the text screen.
19. A missing folder or an unsupported format **MUST** return 1 with a next-step line.
20. A folder with no supported image **MUST** return 0 and **MUST NOT** import the image stack.
21. One failed image **MUST** be reported. The remaining images still run. Any failure makes the exit code 1.
22. The checkout entry `./convert.py` **MUST** call the same conversion.
23. When `outline` or `./convert.py` is about to convert images, this caller **MUST** print the waiting sentence from `requirement-domain-outlineimage` and flush before the blocking call. The choice token is `outline` for the verb and `convert.py` for the script. Returned lines still start with the sentences that were shown. This caller **MUST** print only the remainder, so each sentence appears once. The download sentence is printed only when the weights file is absent, immediately before the fetch, and after the converting sentence. On a terminal, after each of those sentences, this caller **MUST** flash the domain please-wait bullet on the next line and **MUST** erase that line before the next sentence and before the remainder. A stream that is not a terminal **MUST NOT** draw the bullet. `help`, `version`, `about`, and the pip verbs **MUST NOT** announce and **MUST NOT** flash the bullet. The domain file owns the words.

Menu row 1 asks which folder. That question is `requirement-python-tui`. Esc there returns to the front board and does not convert.

### 2.5 Flags

24. The parser accepts the verbs in rule 9. `help` is also available as `--help`.
25. This product does not claim `--json`. **MUST NOT** add it in this file.
26. **MUST NOT** add `--debug`. Debug status is the environment gate on `requirement-python-cli-logging`.
27. **MUST NOT** add a second pair of input paths. The one folder operand belongs to `outline` only.

### 2.6 Output behavior

28. Outline progress and failures **MUST** be visible to the operator. On the text screen they are the result page. Off the text screen they are console lines.
29. Durable status **MUST** go through ChronicleLogger once `main` has constructed it (`requirement-python-cli-logging`). The console failure sentence remains required.
30. **MUST NOT** mix a machine-only JSON mode into the session. This product does not claim `--json`.

### 2.7 No encoder

31. The front board **MUST** be allowed to open when `ffmpeg` is missing. This product does not look for it.
32. `outline` **MUST NOT** spawn an encoder. A missing image library fails only when the folder has a supported image (`requirement-runtime-prerequisites`).
33. The about page runtime-tools line is `none` (`requirement-python-about`). It does not probe `PATH`.

### 2.8 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Console script** | `outline-image = OutlineImage.cli:main` |
| **Module entry** | `src/OutlineImage/__main__.py` → `main()` |
| **CLI module** | `src/OutlineImage/cli.py` defines `Cli` and `def main` in the allowed end state |
| **Empty argv, terminal** | Front board. No conversion. No pip |
| **Empty argv, no terminal** | Help text. Return 0 |
| **Parser** | After ChronicleLogger and the debug block |
| **Quiet / JSON** | Text screen sets `is_quiet=True` on the logger construct. No `--json` |
| **Privilege** | user-level only |
| **Outline** | `Cli._verb_outline` prints the waiting sentence and flushes, flashes the please-wait bullet on a terminal, erases that bullet, then prints only the remainder. It does not draw the menu |
| **Product version** | `1.0.2` |
| **User docs** | Root `README.md` Usage matches this contract |

### 2.9 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: Entry, empty argv, and each typed verb are explicit.
- **Principle 16 – Interactive awareness**: A terminal opens the menu. No terminal prints help and returns 0.
- **Principle 5 – SSOT**: Verb names live here and on the topic owner. The picture lives on the TUI requirement.
- **Principle 10 – Least privilege**: Pip verbs do not use sudo.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, the person runs `outline-image` as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to start the program or to run the pip verbs. Do not pipe a downloaded script into a shell. Type 1 and Type 2 are unused on Termux, Git Bash, and Windows cmd. Git Bash and Windows cmd do not call Termux `pkg`.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** A missing folder does not write an outline. An empty folder does not load the model.
- **Intentional:** Empty argv is the menu on a terminal and help off a terminal.
- **Anti-fragile:** Module entry and the console script both call `main`.
- **Over-protect:** Empty argv does not install, update, or convert a folder.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Change empty argv into a shell-channel install.
2. Make empty argv convert a folder or run pip.
3. Make empty argv off a terminal exit non-zero. That path prints help and returns 0.
4. Remove the console script or the module entry without a packaging and docs update.
5. Require root to run `outline`.
6. Add `hello`, `join`, or `list-videos` without a domain-law change.
7. Add `--json` or `--debug` in this file. `--format` stays on `outline` only.
8. Treat help text as the second mention of a verb.
9. Add `language` as an argv verb. Row 4 is the menu language.
10. Start `outline` or `./convert.py` image work without the domain waiting sentence, print that sentence a second time after it was already shown, announce a download when the weights file is already a file, or leave the please-wait bullet in the result.

**Violating this rule is a critical CLI regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `outline-image` entry declared in packaging |
| AC-2 | `python -m OutlineImage` reaches `main` |
| AC-3 | Empty argv on a terminal opens the front board and does not convert and does not run pip |
| AC-4 | Empty argv with no terminal prints help and returns 0 |
| AC-5 | `outline` does not draw the menu. A folder operand on another verb is an error |
| AC-6 | An empty folder returns 0. A missing folder returns 1 |
| AC-7 | Pip verbs match the command table and do not use sudo or curl |
| AC-8 | `outline` and `./convert.py` print the domain waiting sentence and flush before the work, then print only the remainder. On a terminal the please-wait bullet flashes and is erased when the work finishes. `version` does not announce |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-python-tui` | Menu picture and numbered rows |
| `requirement-python-cli-language` | `language` is not an argv verb. Menu row 4 |
| `requirement-domain-outlineimage` | Outline steps, the folder board, the about domain sentence, and the waiting sentences |
| `requirement-python-about` | The about page |
| `requirement-python-cli-logging` | Construct before the parser |
| `requirement-python-oop` | `Cli` and `def main` |
| `requirement-video-ffmpeg-pipeline` | Retired. This file does not call an encoder |
| `requirement-python-packaging` | Console script name |
| `requirement-python-error-handling` | Fail messaging |
| `requirement-runtime-prerequisites` | Image stack. No encoder check |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-CLI-01** | `tests/test_cli.py` | todo | Empty argv on a tty opens the front board |
| **TP-CLI-02** | `tests/test_outline.py` | have | A folder operand on `version` is an error |
| **TP-CLI-03** | `tests/test_outline.py` | have | An empty directory returns 0 and does not import the image stack |
| **TP-CLI-04** | `tests/test_cli.py` | optional | Empty argv off a tty prints help and returns 0 |
| **TP-TUI-07** | `tests/test_outline.py` | have | Typed `outline` does not open the text screen |
| **TP-CLI-05** | `tests/test_outline.py` | have | `outline` flushes the waiting sentence once before the session. `./convert.py` uses its own choice and prints once. On a terminal the please-wait bullet is erased when the work finishes. `version` does not announce |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Initial Python CLI interface law for OutlineImage |
| 2026-10-04 | Active 1.1.0 | Empty argv opens the text menu on a terminal and prints help off a terminal. Typed verbs. Join questions are the `join` verb |
| 2026-10-04 | Active 1.1.1 | `language` is not an argv verb. Menu row 4 owns it |
| 2026-10-04 | Active 1.1.2 | Verb `about` is `requirement-python-about`. Rule 33 no longer claims a live ffmpeg probe. Product version **1.0.5** |
| 2026-10-05 | Active 1.1.3 | `outline` and `./convert.py` print the domain waiting sentence and flush before the work, then print only the remainder |
| 2026-10-05 | Active 1.1.4 | On a terminal those commands flash the please-wait bullet and erase it when the work finishes |
| 2026-10-07 | Active 1.1.5 | Product version is **1.0.1** |
| 2026-10-10 | Active 1.1.6 | Product version is **1.0.2** |

---

**Last Updated**: 2026-10-10
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
