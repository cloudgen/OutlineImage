**file**: docs/requirements/requirement-domain-outlineimage.md
**Status**: Active (Version 1.3.4)
**Area**: domain
**Key**: `requirement-domain-outlineimage`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This requirement is the domain surface Single Source of Truth for OutlineImage: one chosen folder of images becomes detailed outline images.

Typed verbs and empty argv are owned by `requirement-python-cli-interface`. The screen that shows menu row 1 is owned by `requirement-python-tui`. The conversion functions live in `src/OutlineImage/outline.py`. The about page is `requirement-python-about`.

This file remains the sole Active `requirement-domain-*`. Headings and pictures in the root user document are `requirement-python-readme`.

### 1.1 Human-facing

**In one sentence:** OutlineImage writes a detailed outline image for each picture in a chosen folder. The default file is PNG, in that folder's `output` directory.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person who wants outline images | `outline-image outline` |
| The other role | The text menu, row 1 | `requirement-python-tui` |
| Not this file | The rounded menu frame, pip install, and the log folder | TUI, packaging, and logging requirements |

| Includes | Excludes |
|----------|----------|
| Top-level images in one folder, written as `{stem}_detailed_outline.{ext}` | Joining media, an encoder, a recursive scan |
| Typed `outline`, which converts and does not draw the menu and does not prompt | `hello`, `join`, and `list-videos` as verbs |
| Menu row 1 **outline**: **1** current folder, each immediate subfolder, **0** back, then the same conversion | A second prompt after the folder is chosen |
| One English sentence before converting images, and one before a model download that is about to start. A flashing `• please wait` bullet stays until that work finishes, then it is removed | Saying the model is downloading when that weights file is already present |
| Help and about as real pages | A downloaded-script installer advertised on the about page |

| Surface | What you open | What for |
|---------|---------------|----------|
| `outline-image outline` | The terminal | Convert the current directory. No menu |
| `outline-image outline photos` | The terminal | Convert that folder. No menu |
| Menu row 1 | The folder board, then a result page | Current folder or one subfolder, then the outlines |
| `./convert.py` | A checkout | The same conversion as the verb |
| `outline-image about` | About page | Name, version, what the product does, how to start it |
| `outline-image help` | Help page | The same capabilities, including what this product does not do |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Convert this folder | PNG outlines in `./output`. The menu does not open. The process does not prompt. | `outline-image outline` |
| Convert a named folder | The same, for that folder's own `output` directory. | `outline-image outline photos` |
| Pick from the menu | On a terminal, open the menu and choose **1**. Then **1** is the current folder, the next numbers are subfolders, and **0** returns. Before the conversion starts, the screen says that choice has been selected and that the work takes time. A bullet flashes beside `please wait` until the work finishes, and that bullet is gone on the result page. | `outline-image`, then `1`, then a number |
| Read about | You see OutlineImage, the package version, and the domain sentence. | `outline-image about` |

## 2. Core Rules / Requirements (Mandatory)

### 2.1 Pillar A — The outline verb

`outline` converts one folder. It **MUST NOT** draw the menu and **MUST NOT** prompt. With no folder, the folder is the current directory. The default format is png.

Supported inputs, top level only, are `.webp`, `.png`, `.jpg`, and `.jpeg`. Subfolders are not scanned for images. Output formats are png, webp, jpg, jpeg, bmp, and tiff. Each written file is `{stem}_detailed_outline.{ext}` inside `<folder>/output`, unless the caller passes another output directory. `./convert.py` calls the same function.

| Step ID | User action | Inputs | Output / effect | Ops SSOT |
|---------|-------------|--------|-----------------|----------|
| D-01 | Convert from the terminal | typed verb `outline`, optional folder, optional `--format` | Outline files. Return 0 when the folder exists and every image is written. The menu does not open | this file + CLI |
| D-02 | Convert from the menu | menu row 1, then one folder row | The same conversion. Before it starts, the working page shows the waiting sentence and a flashing please-wait bullet. The lines are the result page. That page does not include the bullet and does not paint the working page again | this file + TUI |

**Routing:** `outline-image outline` **MUST** run D-01 and **MUST NOT** draw the folder board. Front-board row 1 **MUST** open the folder board and **MUST NOT** convert until a folder row is chosen. Bare `outline-image` on a terminal opens the front board and **MUST NOT** run D-01.

**Empty folder:** when the folder exists and has no supported image, the process **MUST** return 0 and **MUST** say no supported images were found. It **MUST NOT** import Pillow, OpenCV, numpy, or rembg for that path.

**Missing folder or bad format:** return 1 and a next-step line. A failure on one image **MUST** be reported and **MUST NOT** stop the remaining images. Any image failure makes the exit code 1. The last line of a run that wrote or tried to write is `Outlines saved in:` plus the output directory.

**Model:** `isnet-general-use`. The longest edge used for the conversion is 1600. The model loads only when the folder has a supported image. The first such run may download that model. A missing image library **MUST** name the pip next step and return 1.

**How the lines are drawn.** This file owns the method. Pillow opens the picture and, when the longest side is longer than 1600, shrinks it. rembg with `isnet-general-use` cuts the object out of the background. OpenCV traces that cutout for the outer shape. A hole is traced when the cutout is transparent there. A very small blob is left out.

Inner lines come from brightness and from color. The cutout is split into lightness and two color channels (CIELAB). A part that matches the object in brightness can still be drawn when its color differs. The color pass stays more sensitive than the brightness pass. The area outside the object is filled with a typical object color before the search, and the search stays inside the object, so the outer shape is drawn once.

Each photo picks its own sensitivity inside a fixed safe range. The range numbers live next to `MAX_EDGE` in `outline.py`. They are not frozen in this file. The program measures how much the foreground already changes from pixel to pixel (a Sobel gradient, then a high percentile of that change). A quiet surface uses the sensitive end of the range, so a faint seam still appears. A scratched or high-contrast photo uses the cautious end, so scuffs stay out. Short specks are dropped. One-pixel breaks in a real seam are closed.

The program draws a line where the photo itself changes. It **MUST NOT** invent a circle, an ellipse, or any other guessed shape to close a gap. A rim that matches the object in both brightness and color may keep a short gap. The root user document explains this method in plain language. The words there match this paragraph.

**Waiting sentence:** This file owns the words. Before converting images, and before downloading the model when that download is about to start, the operator sees one English sentence: `{choice} has been selected. {process} takes time to finish.` The process words are `Converting images` and `Downloading the AI model`. Those process words stay English when the menu language is Chinese. The choice token is the typed verb `outline`, the script name `convert.py`, or the folder-board short: `current` when the pick is `.`, otherwise the child directory name.

Show `Converting images` only when the folder has at least one supported image and the output directory was created, and show it before the image-stack import. Show `Downloading the AI model` only when `model_weights_path()` is not already a file, immediately before the model session, and after the converting sentence. `model_weights_path()` uses `U2NET_HOME` when that variable is set and not blank. Otherwise the directory is `~/.u2net`. The file name is `isnet-general-use.onnx`. An empty folder, a missing folder, a rejected format, and a failed output-directory create do not show either sentence. A missing image library still has the converting sentence and does not add the download sentence. Opening the folder board does not show either sentence. Language, Exit, version, about, help, and the pip lifecycle do not show either sentence.

A function that returns the sentence is enough. Do not store the sentence in a module-level constant. Returned lines lead with the sentences that were shown. On the terminal, a caller that already printed them prints only what follows. On the text screen, the result text may still start with those sentences, and the screen does not paint the working page a second time. The caller rules are `requirement-python-cli-interface` and `requirement-python-tui`.

**Please-wait bullet:** While either process above is running, the operator sees a flashing bullet and the English words `please wait`. The shown line is `• please wait`. The hidden-bullet line is `  please wait`, the same width, so only the bullet flashes. Those words stay English when the menu language is Chinese. A function returns the line. Do not store it in a module-level constant. Show it only after a waiting sentence for that run. Remove it when the conversion returns. The result text does not include it. On a terminal, the bullet is one live line under the sentence. It is erased before the next sentence and before the result lines, so it does not remain. A stream that is not a terminal does not draw it. On the text screen, the working page body is each waiting sentence shown so far, then that bullet line. The page refreshes as the bullet flashes and does not wait for a key. The result page does not include the bullet and does not paint the working page again. Opening the folder board, an empty folder, a missing folder, a rejected format, a failed output-directory create, language, Exit, version, about, help, and the pip lifecycle do not show it.

**Flags:** `--format` / `-f` and a folder operand are legal only on `outline`. On any other verb they are an error. `hello`, `join`, and `list-videos` are unknown verbs.

**Non-goals:** joining media, calling FFmpeg or any other encoder, a shell installer, a recursive image walk, a prompt on the typed verb.

Complete invocation samples this pillar owns:

```text
outline-image outline
outline-image outline photos
outline-image outline --format png
./convert.py
```

### 2.2 Pillar B — The folder board

Menu row 1, kind `outline`, short `outline`, opens layer `folders`.

| Row | Short | Kind | Effect |
|-----|-------|------|--------|
| **1** | `current` | `pick:.` | Convert the current directory |
| **2** … | the directory name | `pick:` plus that name | Convert that immediate child |
| **0** | Back | `back` | Return to the front board. Nothing is converted |

Child rows are immediate directories whose names do not start with `.`, sorted by name ignoring case. `output` and `__pycache__` are listed when they exist. A hidden name is omitted. `.` as a child name, `..`, and a name that contains a separator are refused. Esc on this board returns to the front board.

The explain on row 1 and on each child follows the menu language. The short tokens `outline` and `current`, and each directory name, stay as written. Opening this board does not show the waiting sentence or the please-wait bullet. After a folder pick, and only when pillar A says a process is about to start, the screen shows that sentence and the flashing bullet before the conversion. The result page is the conversion lines. It does not show that waiting page a second time, and it does not keep the bullet. There is no second question.

### 2.3 Pillar C — Help

`outline-image help` and `python -m OutlineImage --help` **MUST** describe folder conversion and **MUST NOT** list `hello`, `join`, `list-videos`, or an encoder. Help is a typed verb. It is not a numbered menu row.

The help page **MUST** include:

| Help row | Text intent |
|----------|-------------|
| Outline | `outline` converts one folder and does not draw the menu. With no folder, it uses the current directory. The default file is png in that folder's `output` directory |
| Menu | On a terminal, `outline-image` with no words shows the front board. Row 1 lists the current folder, each subfolder, and back |
| Absence | This program does not join media and does not require FFmpeg |

### 2.4 Pillar D — About

The domain sentence on the about page is `Write a detailed outline for each image in a folder`. The page, the host check, and the star box are `requirement-python-about`.

| Field | Content |
|-------|---------|
| Product name | OutlineImage |
| Version | `__version__`, the same string as `pyproject.toml` (current `1.0.1`) |
| Domain summary | Write a detailed outline for each image in a folder |

The page **MUST** use that domain sentence. The runtime-tools line **MUST** be `none`. It **MUST NOT** name FFmpeg. Pillow, OpenCV, numpy, and rembg are pip dependencies. They are not a host binary on that line.

### 2.5 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Product / package name** | `OutlineImage` |
| **Console script** | `outline-image` |
| **Checkout entry** | `./convert.py` inserts `src` and calls `OutlineImage.outline.main` |
| **Conversion** | `convert_folder` in `src/OutlineImage/outline.py` |
| **Menu row** | Front row 1, kind `outline`, short `outline`. Folder board layer `folders` |
| **Output** | `<folder>/output/{stem}_detailed_outline.png` by default |
| **Inputs** | `.webp` `.png` `.jpg` `.jpeg`, this folder only |
| **VERSION** | `1.0.1` (`__init__.py` and `pyproject.toml`) |
| **Absent** | `src/OutlineImage/join.py`, verbs `hello`, `join`, and `list-videos`, FFmpeg |
| **CLI SSOT** | `requirement-python-cli-interface` |
| **Screen** | `requirement-python-tui` |
| **User docs** | Root `README.md` |

### 2.6 Why This Requirement Exists (CIAO)

- **Principle 2 – Intentional**: The folder and the format are explicit. Empty argv does not convert.
- **Principle 5 – SSOT**: One Active domain file. One conversion function for the verb, the menu, and `./convert.py`.
- **Principle 1 – Caution**: An empty folder does not load the model. A missing folder fails closed. Source images are not deleted.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, `outline` and the menu run as the normal user. **This requirement:** do not use administrator privilege, `sudo`, `apt`, or a dedicated system user to write an outline image. Do not pipe a downloaded script into a shell.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** Do not load the model when the folder has no supported image.
- **Intentional:** One conversion, two surfaces, one default format.
- **Anti-fragile:** README, help, about, the terminal, and row 1 name the same output.
- **Over-protect:** Keep the sole Active domain file.

## 4. Protection Rule (Sacred)

**Future AI assistants, Grok, or maintainers MUST NOT**:

1. Add `hello`, `join`, `list-videos`, or FFmpeg without an explicit user order and a new revision of this file.
2. Add a shell installer or root elevation as silent domain behavior.
3. Create a second Active `requirement-domain-*` without superseding this one.
4. Make the typed verb prompt, or make empty argv start a conversion.
5. Scan subfolders for images, or write outlines somewhere other than `<folder>/output` unless the caller passed an output directory.
6. Import the image stack when the chosen folder has no supported image.
7. Start a conversion or a model fetch without the waiting sentence in pillar A, show a download sentence when the weights file is already a file, show either sentence for an empty folder, a missing folder, a rejected format, or a failed output-directory create, or store the sentence in a module-level constant.
8. Leave the please-wait bullet on the result, show it when no waiting sentence was shown, or store that bullet line in a module-level constant.
9. Replace a detected edge with a fitted circle or ellipse, or draw a guessed shape across a gap. A rim that matches the object in both brightness and color may keep a short gap.

**Violating this rule is a critical domain regression.**

## 5. Acceptance criteria

| ID | Criterion |
|----|-----------|
| AC-1 | `outline-image outline` converts the current directory, does not draw the menu, and does not prompt |
| AC-2 | The default file is PNG, named `{stem}_detailed_outline.png`, in `<folder>/output` |
| AC-3 | Menu row 1 is `outline`. The next board is **1** current folder, numbered subfolders, and **0** back |
| AC-4 | `hello`, `join`, and `list-videos` are unknown verbs |
| AC-5 | An empty folder returns 0 and does not import the image stack |
| AC-6 | Help and about do not describe a join or an encoder. The domain sentence is the one in pillar D |
| AC-7 | This file stays the sole Active domain SSOT |
| AC-8 | Before converting images, and before a model download when the weights file is absent, the operator sees the pillar A sentence for that process. An empty folder, a missing folder, a rejected format, a failed output-directory create, and a weights file that is already present do not announce a download. The sentence is not a module-level constant |
| AC-9 | While that process runs, a bullet flashes beside `please wait`. The bullet is gone when the process finishes. The result text does not include it |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `requirement-video-ffmpeg-pipeline` | Retired. Do not restore |
| `requirement-python-cli-interface` | Typed `outline`, `--format`, and the folder operand |
| `requirement-python-about` | About page. This file keeps the domain sentence |
| `requirement-python-tui` | Row 1 opens the folder board |
| `requirement-python-oop` | `outline.py` holds the conversion functions |
| `requirement-python-dependency-management` | Pip strings for the image stack and ChronicleLogger |
| `requirement-python-packaging` | Manifest shape |
| `requirement-runtime-prerequisites` | Those pip packages. No encoder |
| `requirement-python-error-handling` | Missing folder, bad format, one failed image |
| `requirement-class-software-dev` | Class residual |
| `requirement-python-readme` | Headings and pictures in the user document |
| `docs/requirements/index.md` | Registry |

## Design-time verification

| TP family / ID | Suite | Status | Note |
|----------------|-------|--------|------|
| **TP-OUTLINE-01** | `tests/test_outline.py` | have | `outline` is a verb. `hello`, `join`, and `list-videos` are not. The verb does not open the menu |
| **TP-OUTLINE-02** | `tests/test_outline.py` | have | An empty directory returns 0 and does not import the image stack. A missing folder returns 1 |
| **TP-OUTLINE-03** | `tests/test_outline.py` | have | Row 1 opens the folder board: current, sorted children, back |
| **TP-OUTLINE-04** | `tests/test_outline.py` | have | The sentence names the choice and the process. Converting is announced before the download. A weights file that is already present does not say the model is downloading. A bad format, a failed output directory, and a missing import stay honest |
| **TP-OUTLINE-05** | `tests/test_outline.py` | have | The please-wait bullet flashes during the conversion and is absent from the result. On a terminal the live line is erased when the work finishes |

**Matrix:** `docs/reviews/requirement-test-matrix.md`
**Map:** `docs/reviews/test-plan.md`

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-08-09 | Active 1.0.0 | Domain SSOT for OutlineImage interactive two-file join |
| 2026-10-04 | Active 1.1.2 | Pillar D kept the join domain sentence. Product version **1.0.5** |
| 2026-10-05 | Active 1.2.0 | The domain is the welcome line. Join, file listing, and FFmpeg are non-goals |
| 2026-10-05 | Active 1.3.0 | The domain is a detailed outline image. Typed `outline` and menu row 1. Product version **1.0.0** |
| 2026-10-05 | Active 1.3.1 | Waiting sentence before converting images and before a model download. Product version stays **1.0.0** |
| 2026-10-05 | Active 1.3.2 | A flashing `• please wait` bullet stays while that process runs and is removed when it finishes. Product version stays **1.0.0** |
| 2026-10-07 | Active 1.3.3 | Lines come from brightness and color. Each photo picks a sensitivity inside a safe range. Short specks are dropped. A guessed circle or ellipse is refused. Product version stays **1.0.0** |
| 2026-10-07 | Active 1.3.4 | Product version is **1.0.1** |

---

**Last Updated**: 2026-10-07
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
