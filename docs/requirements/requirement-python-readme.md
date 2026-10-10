**file**: docs/requirements/requirement-python-readme.md
**Status**: Active (Version 1.0.6)
**Area**: python
**Key**: `requirement-python-readme`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file owns the product user document at the repository root: which sections it has, which pictures it embeds, and the rule that a sentence in that document matches the requirement that owns the behavior. Project nature is a program a person builds and runs from a terminal. The menu picture stays on `requirement-python-tui`. The thirteen languages stay on `requirement-python-cli-language`. The verbs stay on `requirement-python-cli-interface`. The outline stays on `requirement-domain-outlineimage`. The encoder file is Retired. The prerequisite sentences stay on `requirement-runtime-prerequisites`. The package name and the console script stay on `requirement-python-packaging`. The version string is `__version__`. This file does not restate those bodies.

### 1.1 Human-facing

**In one sentence:** You open the root user document to install the program, read how a folder becomes outline images, and see pictures of this program.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | The person reading how to run the program | Open `README.md` at the checkout root |
| The other role | The requirements that own the menu, the outline, and the package | A sentence here matches those files |
| Not this file | The concat itself, the language file, and the host check | Pipeline, language, and domain |

| Includes | Excludes |
|----------|----------|
| Section order, badges, the Advantages contrast, install sentences, and the picture catalog | A second menu, a second verb list, or a second encode order |
| Absolute `https` image destinations for captures of the running text menu | A generated drawing that invents row text. A relative `screenshots/` image destination in this package description |
| The eight related-project lines | A shell online install, root as the documented path, or a setup script that is not on disk |

| Surface | What you open | What for |
|---------|---------------|----------|
| `README.md` | Root user document | Install, usage, pictures |
| `screenshots/` | Picture folder beside that document | The links in the Screenshots section |
| `outline-image` | The program on a terminal | What those pictures show |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Read the install | The public path is pip. The document does not ask for root. | `pip install OutlineImage` |
| Check the pictures | Row 4 is the language list. The current board is row 1 outline. About stays in English. | `outline-image`, then `4`, or `1` |
| Check the version line | The badge matches the package string. | `outline-image version` |

## 2. Core Rules / Requirements (Mandatory)

The user document is how a person learns the program. It is not a second copy of product law. A claim in the document matches the requirement that owns that claim.

### 2.1 Where it lives

1. **MUST** keep the user document at the repository-root `README.md`. Product law stays under `docs/requirements/`. The layout rule that the file exists is `requirement-python-project-structure`. This file owns the sections and the pictures.
2. Pictures **MUST** live in a `screenshots/` folder at that same root. The user document **MUST** link every PNG in that folder. This document is the package description. Each image destination **MUST** be an absolute `https` URL that names that PNG on the public source host. A relative `screenshots/<file>` destination fails on the package index: the index fetches that path on its own host, and the picture folder is not in the published archive. The same relative destination still opens on the source forge. A link to a sibling document, such as `LICENSE.md`, **MAY** stay relative. A PNG on disk and absent from `README.md` fails this file. The URL base for this product is in Implementation Notes. That URL does not render on the package index until the file is on the public branch named in the URL.
3. **MUST NOT** freeze a session login or a `/home/<login>/` path in this requirement or in a sentence that is law. A picture may show the directory where that capture was started. The sentence in the document names “the current directory.”

### 2.2 What the document contains

The document **MUST** keep the sections in §2.5, in that order. A new heading, a dropped heading, or a reordered heading is a revision of this file.

Each behavioral sentence **MUST** match its owner and **MUST NOT** restate that owner’s procedure:

| Claim in the document | Owner |
|-----------------------|--------|
| Folder conversion, default png, `<folder>/output` | `requirement-domain-outlineimage` |
| How an outline is drawn: Pillow, rembg `isnet-general-use`, OpenCV brightness and color, a sensitivity per photo, a brightness shadow step and a bright middle left out, a thin dark groove kept, speck removal, and no guessed shape | `requirement-domain-outlineimage` |
| No encoder | `requirement-video-ffmpeg-pipeline` is Retired |
| Menu picture, path row, clock, row numbers | `requirement-python-tui` |
| Thirteen languages and what stays English | `requirement-python-cli-language` |
| Product verbs and pip lifecycle commands | `requirement-python-cli-interface` |
| Empty argv on a terminal opens the menu. Empty argv with no terminal prints help and returns 0. Typed `outline` converts and does not draw the menu | `requirement-python-cli-interface` |
| Package name, console script, pip install | `requirement-python-packaging` |
| Package string on the badge | `__version__` in `src/OutlineImage/__init__.py`, copied by `pyproject.toml` |
| `ChronicleLogger>=1.3.1` and the image floors | `requirement-python-dependency-management` |
| Pip image stack, no host encoder, no root auto-install | `requirement-runtime-prerequisites` and `requirement-python-dependency-management` |

This product does not claim `--json`. `outline` is a product verb. `hello` is not. The user document does not name `./setup.sh` or `./build.sh`.

The first-row sentence in the user document **MUST** name the current directory on the left and a local clock (`HH:MM:SS`) on the right when the row has room. It **MUST NOT** name `Current`, a login, `USER`, `USERNAME`, or `getpass` as that right-hand field. The picture of the row stays on `requirement-python-tui`.

### 2.3 Pictures

1. A menu picture **MUST** be a capture of the running text menu. **MUST NOT** satisfy a menu row with a drawing that invents row text. Every PNG in `screenshots/` **MUST** be linked from the user document. A PNG that is not a menu capture **MUST** be labeled as that file and **MUST NOT** be described as a text-menu capture.
2. The Screenshots section **MUST** show every PNG in `screenshots/`, in the catalog order. The lead **MUST** say that the menu pictures are captures of this program and that row 1 is **outline**. `source-photo.png` and `outline-result.png` are not text-menu captures.
3. A paragraph **MUST** quote the pixels. It **MUST NOT** be rewritten so that an old picture appears to say OutlineImage when the pixels say VideoJoin. The current conversion is not those pictures. The domain file owns `{stem}_detailed_outline.png`.
4. The about picture **MUST** stay in English. Leaf shorts in every menu picture **MUST** stay the English verb. That split is `requirement-python-cli-language`.
5. A live-menu capture satisfies this file when it shows the menu the program paints, including a double-width label that stays whole and a clock that stays on the path row.
6. The heading of each picture **MUST** be that file’s basename. The paragraph and the image alt **MUST** be the catalog cells for that file. Those words come from the basename and from what the picture shows: the words on the screen, the characters in the input box, or the scene. A language name alone, or a sentence that only says the file is a picture, fails this file. The paragraph **MUST NOT** freeze a session login or a `/home/<login>/` path. The path row is “the current directory.”

### 2.4 Install honesty

1. The public install path **MUST** be pip. **MUST NOT** document a shell online install, `sudo pip`, or `sudo curl | sh`.
2. **MUST NOT** name a checkout setup script that is not on disk. This tree has no `setup.sh`. The document **MUST NOT** name `setup.sh`.
3. The document does not show a wheel or sdist example. **MUST NOT** add one unless the basename is the file the build writes and the version token matches the package version.
4. The prerequisite sentences **MUST** stay aligned with `requirement-runtime-prerequisites`. This file **MUST NOT** copy that table as a second owner.
5. **MUST NOT** add `./build.sh` verbs to the user document. Those verbs are not `outline-image` verbs.

### 2.5 Implementation Notes (this project)

| Field | Value |
|-------|--------|
| **Document** | `README.md` |
| **Pictures** | `screenshots/` |
| **Package** | `OutlineImage` |
| **Console script** | `outline-image` |
| **Version** | `1.0.2` from `src/OutlineImage/__init__.py` (`__version__`). `pyproject.toml` copies that string |
| **Python** | `>=3.10`. The badge says 3.10+ |
| **License file** | `LICENSE.md` (MIT). The file is present. The document link stays relative |
| **Homes** | `https://github.com/cloudgen/OutlineImage` and `https://pypi.org/project/OutlineImage/` |
| **Current job** | `outline-image outline` writes `{stem}_detailed_outline.png` in `<folder>/output` |
| **Every PNG** | `README.md` links each PNG under `screenshots/`. `source-photo.png` and `outline-result.png` are linked and are not menu captures |
| **Image URL** | `https://raw.githubusercontent.com/cloudgen/OutlineImage/main/screenshots/<basename>`. The package index can fetch that file only after it is on that public branch |

**Title:** `OutlineImage - Detailed outline images from a folder`.

**Badges:** a Version badge whose token is the package string; License MIT; CIAO linked to `https://github.com/cloudgen/ciao`; stars for `cloudgen/OutlineImage`; Python 3.10+; PyPI `OutlineImage` linked to `https://pypi.org/project/OutlineImage/`.

**Opening:** write a detailed outline image for each picture in a folder. The default file is PNG, in an `output` folder next to those pictures. On a terminal with no arguments, the text menu opens. The menu does not convert images by itself and does not call pip.

**Sections, in order.** Advantages is inserted after Features. How an outline is made is inserted after Advantages. Screenshots is inserted after Usage. The other headings keep the existing kit order.

| Heading | What this document must keep | Owner of the behavior |
|---------|------------------------------|------------------------|
| Features | Text menu: outline, system-log, language, self-management, Exit. Path and a local clock on the first row. Row 1 lists the current folder, each subfolder, and back. system-log is **3**. language is **4**. self-management is **8**. Verbs `help`, `version`, `about`, `outline`, `self-install`, `version-check`, `self-update`, `self-uninstall`. Checkout entry `./convert.py` | Peers in §2.2. The path-row sentence is the clock rule in §2.2 |
| Advantages | The four parts and the comparison table below | This file for the contrast. Peers in §2.2 for the behavior |
| How an outline is made | Plain language for the method in `requirement-domain-outlineimage`: Pillow shrinks the long side to 1600, rembg with `isnet-general-use` cuts the object out, NumPy holds the pixels, and OpenCV draws the outer shape plus inner lines from brightness and from color (CIELAB). Canny uses a Sobel measurement so each photo picks a sensitivity inside a safe range. Color stays more sensitive than brightness. A brightness step whose sides do not match is left out, and so is a line that is bright in the middle. A thin dark groove stays. Color lines and the outer shape skip that check. Short specks are dropped. A rim that matches the object in brightness and color can keep a short gap. A guessed circle or oval is not used | `requirement-domain-outlineimage` for the method. This file for the section |
| Quick Installation | `ChronicleLogger>=1.3.1`, `numpy>=2.3.0`, `Pillow>=12.1.0`, `opencv-python-headless>=5.0.0.93`, and `rembg>=2.0.85`. `pip install OutlineImage`. No external media tool. Checkout uses a venv and `pip install -e .`. The fenced text menu (front, system-log, language, self-management) stays in this section and shows row 1 **outline** and version **1.0.2** | `requirement-python-dependency-management`, `requirement-runtime-prerequisites`, `requirement-python-packaging`, `requirement-python-tui` |
| Usage | Menu versus typed verbs. `outline` converts a folder and does not draw the menu. Menu row 1 lists the current folder, each subfolder, and back. Default PNG in that folder's `output` directory. No terminal: empty argv prints help and returns 0. `self-uninstall` needs `--force`. No sudo | `requirement-python-cli-interface`, `requirement-domain-outlineimage`, `requirement-python-tui` |
| Screenshots | Lead: each heading is the file name, and the paragraph is what that picture shows. Package **1.0.0**. The paragraph and the image alt are the catalog below. The menu pictures are captures of this program. Row 1 is **outline** | This file |
| Examples | `cd` to a folder of images, then `outline-image`, then `outline-image version`, then `outline-image outline` | `requirement-domain-outlineimage` |
| Platform Compatibility | Linux primary. macOS and Windows when CPython is present. The text menu needs a terminal | `requirement-runtime-prerequisites` |
| Related Projects | The eight lines below, in that order, each with one sentence | This file |
| Contributing | Keep product law in sync. The conversion lives in `src/OutlineImage/outline.py`. Version strings stay together | `requirement-python-coding-style`, `requirement-python-packaging` |
| License | MIT, link `LICENSE.md`, and that file exists | `requirement-python-packaging` |
| Last Update | Names package **1.0.2**, the public source `https://github.com/cloudgen/OutlineImage`, the outline conversion, that lines use brightness and color with a per-photo sensitivity, that a brightness shadow step and a bright middle are left out, and that the Screenshots section shows captures of this program | This file for the line. `__version__` for the string |

**Related projects, in this order.** The first two are this program. Each line is one sentence. Do not add an install recipe.

| Order | Link | Sentence |
|------:|------|----------|
| 1 | `https://github.com/cloudgen/OutlineImage` | This program’s source |
| 2 | `https://pypi.org/project/OutlineImage/` | This program on PyPI |
| 3 | `https://github.com/Wilgat/AnimeDlp` | Command-line downloader for anime video sites |
| 4 | `https://github.com/Wilgat/ChronicleLogger` | Status logger this program depends on (`ChronicleLogger>=1.3.1`) |
| 5 | `https://github.com/Wilgat/VideoSpeed` | Cuts, changes speed, and boomerangs a clip. That program is not this one |
| 6 | `https://github.com/cloudgen/ciao` | Caution, Intentional, Anti-fragile, Over-engineered |
| 7 | `https://github.com/cloudgen/ciao-lite` | Short agent contract |
| 8 | `https://github.com/cloudgen/safe-rm` | Guarded `rm` |

**Advantages, after Features and before Quick Installation.** Three parts. The path row in Features names the local clock. There is no FFmpeg comparison table.

1. **A folder in, outlines out.** `outline-image outline` converts images in the current directory and does not draw the menu. On the menu, row **1 outline** asks for the current folder or a subfolder, then writes PNG outlines in that folder's `output` directory. There is no `--json`. With no arguments on a terminal, the text menu opens. With no terminal and no verb, the program prints help and returns 0.
2. **Built-in languages.** Row **4** lists thirteen languages: English, Simplified Chinese, Traditional Chinese, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Dutch, and Greek. The choice is saved for the next run.
3. **Lifecycle and diagnostics.** `version-check`, `self-update`, `self-install`, and `self-uninstall` are menu rows **84**–**87** and typed verbs. `self-uninstall` on the command line needs `--force`. They call pip and do not use root. **system-log** (**3**) views a log, clears a log, and shows the log folder. **about** (**83**) stays in English. The document does not include an FFmpeg comparison table.

**Screenshot catalog, in this order.** Each image destination is the absolute `https` URL in Implementation Notes, with that file’s basename. The paragraph and the alt are the words `README.md` prints for that file. The menu pictures are captures of this program. A picture that is not a menu capture says so.

| Order | File | Paragraph | Alt |
|------:|------|-----------|-----|
| 1 | `language-menu.png` | Row **4** has opened the language list. **41 English** is highlighted, with the note "use English for this menu." The other rows are **42 简体中文**, **43 繁體中文**, **44 Español**, **45 العربية**, **46 Français**, **47 Português**, **48 Русский**, **49 Deutsch**, **50 日本語**, **51 한국어**, **52 Nederlands**, and **53 Ελληνικά**. Each note says to use that language for this menu. Arabic on row 45 reads right to left, and the number stays on the left. **0 Back** says "return to the main menu." The path label is `Path`. The path row names the current directory. The clock is `16:57:38` on the right of that row. The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `language`. | Language list, 41 English highlighted |
| 2 | `main-menu-en.png` | English main menu. There is no saved-language line above the box. The path label is `Path`. The path row names the current directory. The clock is `16:55:35` on the right of that row. **1 outline** is highlighted: "convert images in a chosen folder to outlines." Then **3 system-log** "view, clear, and the log folder," **4 language** "display language for this menu," **8 self-management** "version, about, and pip lifecycle," and **9 Exit** "leave." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `main menu`. | English main menu, 1 outline highlighted |
| 3 | `main-menu-zh-hans.png` | Simplified Chinese main menu. The line above the box says `菜单语言是简体中文`. The path label is `路径`. The path row names the current directory. The clock is `16:55:38` on the right of that row. **1 outline** is highlighted and stays `outline`: "把所选文件夹中的图像转为轮廓." **3** is `系统日志` "查看、清空，以及日志文件夹," **4** is `语言` "此菜单的显示语言," **8** is `自我管理` "版本、关于，以及 pip 生命周期," and **9** is `离开` "离开." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `主菜单`. | Simplified Chinese main menu, 1 outline highlighted |
| 4 | `main-menu-zh-hant.png` | Traditional Chinese main menu. The line above the box says `選單語言是繁體中文`. The path label is `路徑`. The path row names the current directory. The clock is `16:55:39` on the right of that row. **1 outline** is highlighted and stays `outline`: "把所選資料夾中的影像轉為輪廓." **3** is `系統日誌` "查看、清空，以及日誌資料夾," **4** is `語言` "這個選單的顯示語言," **8** is `自我管理` "版本、關於，以及 pip 生命週期," and **9** is `離開` "離開." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `主選單`. | Traditional Chinese main menu, 1 outline highlighted |
| 5 | `main-menu-es.png` | Spanish main menu. The line above the box says `El idioma del menú es español`. The path label is `Ruta`. The path row names the current directory. The clock is `16:55:40` on the right of that row. **1 outline** is highlighted and stays `outline`: "convierte las imágenes de una carpeta elegida en contornos." **3** is `registro` "ver, vaciar y la carpeta de registro," **4** is `idioma` "idioma de este menú," **8** is `autogestión` "versión, acerca de y el ciclo de pip," and **9** is `Salir` "salir." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `menú principal`. | Spanish main menu, 1 outline highlighted |
| 6 | `main-menu-ar.png` | Arabic main menu. The line above the box says `لغة القائمة هي العربية`. The path label is `المسار`. The path row names the current directory. The clock is `16:57:07` on the right of that row. The numbers stay on the left. Arabic phrases are shaped and read right to left. **1 outline** is highlighted and stays `outline`: "حوّل صور المجلد المختار إلى حدود." **3** is `سجل النظام` "عرض ومسح ومجلد السجل," **4** is `لغة` "لغة العرض لهذه القائمة," **8** is `إدارة ذاتية` "الإصدار وحول ودورة pip," and **9** is `خروج` "خروج." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `القائمة الرئيسية`. | Arabic main menu, 1 outline highlighted |
| 7 | `main-menu-fr.png` | French main menu. The line above the box says `La langue du menu est le français`. The path label is `Chemin`. The path row names the current directory. The clock is `16:55:41` on the right of that row. **1 outline** is highlighted and stays `outline`: "convertit les images d'un dossier choisi en contours." **3** is `journal` "voir, vider et le dossier du journal," **4** is `langue` "langue d'affichage de ce menu," **8** is `autogestion` "version, à propos et le cycle pip," and **9** is `Quitter` "quitter." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `menu principal`. | French main menu, 1 outline highlighted |
| 8 | `main-menu-pt.png` | Portuguese main menu. The line above the box says `O idioma do menu é português`. The path label is `Caminho`. The path row names the current directory. The clock is `16:55:42` on the right of that row. **1 outline** is highlighted and stays `outline`: "converte as imagens de uma pasta escolhida em contornos." **3** is `registo` "ver, esvaziar e a pasta de registo," **4** is `idioma` "idioma deste menu," **8** is `autogestão` "versão, acerca de e o ciclo do pip," and **9** is `Sair` "sair." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `menu principal`. | Portuguese main menu, 1 outline highlighted |
| 9 | `main-menu-ru.png` | Russian main menu. The line above the box says `Язык меню — русский`. The path label is `Путь`. The path row names the current directory. The clock is `16:55:43` on the right of that row. **1 outline** is highlighted and stays `outline`: "преобразовать изображения выбранной папки в контуры." **3** is `системный журнал` "просмотр, очистка и папка журнала," **4** is `язык` "язык этого меню," **8** is `самоуправление` "версия, о программе и цикл pip," and **9** is `Выход` "выход." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `главное меню`. | Russian main menu, 1 outline highlighted |
| 10 | `main-menu-de.png` | German main menu. The line above the box says `Die Menüsprache ist Deutsch`. The path label is `Pfad`. The path row names the current directory. The clock is `16:55:44` on the right of that row. **1 outline** is highlighted and stays `outline`: "Bilder eines gewählten Ordners in Umrisse umwandeln." **3** is `Systemprotokoll` "ansehen, leeren und der Protokollordner," **4** is `Sprache` "Anzeigesprache für dieses Menü," **8** is `Selbstverwaltung` "Version, Info und pip-Lebenszyklus," and **9** is `Beenden` "beenden." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `Hauptmenü`. | German main menu, 1 outline highlighted |
| 11 | `main-menu-ja.png` | Japanese main menu. The line above the box says `メニューの言語は日本語`. The path label is `パス`. The path row names the current directory. The clock is `16:55:44` on the right of that row. **1 outline** is highlighted and stays `outline`: "選んだフォルダの画像を輪郭にする." **3** is `システムログ` "表示、消去、ログフォルダ," **4** is `言語` "このメニューの表示言語," **8** is `自己管理` "バージョン、概要、pip のライフサイクル," and **9** is `終了` "終了." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `メインメニュー`. | Japanese main menu, 1 outline highlighted |
| 12 | `main-menu-ko.png` | Korean main menu. The line above the box says `메뉴 언어는 한국어`. The path label is `경로`. The path row names the current directory. The clock is `16:55:45` on the right of that row. **1 outline** is highlighted and stays `outline`: "고른 폴더의 이미지를 윤곽으로 바꿉니다." **3** is `시스템 로그` "보기, 비우기, 로그 폴더," **4** is `언어` "이 메뉴의 표시 언어," **8** is `자기관리` "버전, 정보, pip 수명 주기," and **9** is `종료` "종료." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `주 메뉴`. | Korean main menu, 1 outline highlighted |
| 13 | `main-menu-nl.png` | Dutch main menu. The line above the box says `De menutaal is Nederlands`. The path label is `Pad`. The path row names the current directory. The clock is `16:55:46` on the right of that row. **1 outline** is highlighted and stays `outline`: "zet afbeeldingen in een gekozen map om in contouren." **3** is `systeemlog` "bekijken, legen en de logmap," **4** is `taal` "weergavetaal voor dit menu," **8** is `zelfbeheer` "versie, info en de pip-levenscyclus," and **9** is `Afsluiten` "afsluiten." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `hoofdmenu`. | Dutch main menu, 1 outline highlighted |
| 14 | `main-menu-el.png` | Greek main menu. The line above the box says `Η γλώσσα του μενού είναι ελληνικά`. The path label is `Διαδρομή`. The path row names the current directory. The clock is `16:55:47` on the right of that row. **1 outline** is highlighted and stays `outline`: "μετατρέπει τις εικόνες ενός φακέλου σε περιγράμματα." **3** is `αρχείο καταγραφής` "προβολή, εκκαθάριση και ο φάκελος καταγραφής," **4** is `γλώσσα` "γλώσσα εμφάνισης για αυτό το μενού," **8** is `αυτοδιαχείριση` "έκδοση, σχετικά και ο κύκλος του pip," and **9** is `Έξοδος` "έξοδος." The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `κύριο μενού`. | Greek main menu, 1 outline highlighted |
| 15 | `outline-folders.png` | Row **1 outline** has opened the folder board. **1 current** is highlighted: "convert images in this folder." **2 photos** says "convert images in this subfolder." **0 Back** says "return to the main menu." The path label is `Path`. The path row names the current directory. The clock is `16:55:38` on the right of that row. The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `outline`. | Folder board, 1 current highlighted |
| 16 | `self-management.png` | Row **8** has opened self-management. **82 version** is highlighted: "show the installed version." Then **83 about** "version and this computer," **84 version-check** "compare this install with pip," **85 self-update** "upgrade this package with pip," **86 self-uninstall** "remove this package with pip," **87 self-install** "install this package with pip," and **0 Back** "return to the main menu." The path label is `Path`. The path row names the current directory. The clock is `16:55:36` on the right of that row. The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `self-management`. | Self-management, 82 version highlighted |
| 17 | `tui-about.png` | **about** (83) on the result page. The title is `OutlineImage (1.0.0) — result`. The page prints `OutlineImage 1.0.0`, `Domain: Write a detailed outline for each image in a folder`, `Runtime tools: none`, and `Entry points: outline-image, python -m OutlineImage`. The host check is stamped `2026-10-05 16:55:47.777304` and headed `[CHECK SYSTEM]:`. Visible lines include Python 3.12.11, C Library GCC 13.3.0, Ubuntu 24.04.5 LTS, amd64, the current user, the shell `/bin/bash`, `Inside docker container: False`, `Cython String: cpython-312-x86_64-linux-gnu`, `Binary Type: amd64-glibc`, and `TTY / Interactive: yes`. The star box says `OutlineImage (1.0.0) by Wilgat Wong on 2026-10-05`, `You are using an UNINSTALLED version`, `Basic Usage:` then `outline-image outline`, and `Please visit our homepage:` then `"https://github.com/cloudgen/OutlineImage"`. The footer says `Press a key to return to the main menu.` There is no input box and no clock. The page stays in English. | About host check, English, homepage cloudgen/OutlineImage |
| 18 | `system-log.png` | Row **3** has opened system-log. **31 view-log** is highlighted: "list a log file and show it." Then **32 clear-log** "empty one log file," **33 log-folder** "show the log folder," and **0 Back** "return to the main menu." The path label is `Path`. The path row names the current directory. The clock is `16:55:37` on the right of that row. The input box shows `>` and is otherwise empty. The status line says `OutlineImage 1.0.0` and `system-log`. | System log, 31 view-log highlighted |
| 19 | `source-photo.png` | A photograph, not a text-menu capture. A bright green plastic phone stand, with a grey hinge knob and two dark pads, sits on a pale surface. A round hole and a slot are cut into the stand. Behind it is a white board with a fine grid. | Green phone stand on a pale surface, source photograph |
| 20 | `outline-result.png` | A generated outline image, not a text-menu capture. White contour lines on a black field draw the same phone stand: the back plate, the hinge knob, the two pads, the round hole, and the slotted base. | White contour of the phone stand on black |

`TP-DOC-01` asserts the Version badge token, that every PNG is linked with the absolute `https` URL above, that no markdown image uses a relative `screenshots/` destination, that the section headings are present, that the document does not name `setup.sh`, that the eight related-project URLs are in order, that the path row names the local clock, and that `source-photo.png` and `outline-result.png` are not described as text-menu captures. `TP-DOC-03` asserts that each screenshot paragraph and alt equals the catalog cell, and it does not claim a pixel-by-pixel proof. `TP-DOC-03` stays **todo**. Map: `docs/reviews/test-plan.md`.

### 2.6 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The sections and every PNG in `screenshots/` are a named catalog. A later edit cannot drop the language list, leave a PNG unlinked, or swap in a drawing for a menu row.
- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): This file owns the document. Behavior stays on the peer that already owns it.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): The pictures show a text menu, including row **4**, the folder board, self-management, about, and system-log. The photograph and the outline image stay labeled as themselves.
- **CIAO Principle 21 – Dual policies** (https://github.com/cloudgen/ciao): The portable rule is “the document matches its owner.” The OutlineImage headings and file names live in §2.5.
- **CIAO Principle 4 – Over-protect** (https://github.com/cloudgen/ciao): Do not publish a setup script that is not on disk, or a success line the program did not print.

## Under command line for normal user only

The documented install is for this login. **This requirement:** the user document **MUST NOT** tell the reader to use `sudo`, `sudo pip`, `sudo curl | sh`, or a dedicated system account. Git Bash and Windows cmd **MUST NOT** be told to invoke Termux `pkg`. The public install path is pip. A picture does not change who may run a verb.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** An install sentence that names a missing script is a defect.
- **Intentional:** An Advantages section, twenty pictures, one section order. Each picture paragraph is the catalog cell for that file.
- **Anti-fragile:** A new PNG in `screenshots/` becomes a required link in the same change. A non-menu file stays labeled as itself.
- **Over-protect (Principle 20):** Do not let the user document become a second menu, a second verb list, or a second encode procedure.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT**:

- Restate encode order, verb lists, menu numbers, language codes, or the prerequisite table in this file as a second procedure.
- Turn the Advantages section into an FFmpeg filter recipe. The concat graph may be named only as something the person does not write.
- Claim that intermediate files never use the system temporary directory.
- Replace a capture with a drawing that invents row text.
- Leave any PNG in `screenshots/` out of `README.md`.
- Use a relative `screenshots/` destination for a picture in this package description. The package index cannot fetch that path. A sibling-document link such as `LICENSE.md` may stay relative.
- Describe `screenshots/source-photo.png` or `screenshots/outline-result.png` as a text-menu capture.
- Caption a picture with only a language name, or with a sentence that does not say what the picture shows.
- Describe the path row’s right side as `Current` or a login.
- Name `./setup.sh` while that file is absent.
- Add `./build.sh` verbs, a shell online install, `sudo pip`, or `sudo curl | sh` to the user document.
- Add `--json`, a length percent, a boomerang, or a folder prompt.
- Freeze a session login or a `/home/<login>/` path in this file.
- Mark `TP-DOC-03` have before the suite asserts that each catalog paragraph and alt equals the cell in §2.5.
- Treat `./build.sh` verbs as `outline-image` verbs.

## 5. Definition of done

1. `README.md` has the sections in §2.5, in that order, including Advantages after Features, How an outline is made after Advantages, and Screenshots after Usage.
2. The Version badge token matches the package string.
3. The Screenshots section links every PNG in `screenshots/`, in catalog order, including `source-photo.png` and `outline-result.png`. Each image destination is an absolute `https` URL. Each heading is the basename. Each paragraph and each image alt are the catalog cells for that file.
4. The path-row sentence names the local clock.
5. The document does not name `setup.sh`, `sudo pip`, or a shell online install.
6. Related Projects lists the eight URLs in §2.5, in that order.
7. `TP-DOC-01` is **have** in `tests/test_docs.py` (`./tests/run.sh`, 7 tests, OK). `TP-DOC-03` stays **todo** until the suite asserts that each paragraph and alt equals the catalog cell.

### Design-time verification

| TP family / ID | Suite | Status |
|----------------|-------|--------|
| **TP-DOC-01** Version badge matches the package string. Every PNG uses the absolute `https` URL. No relative `screenshots/` image. Section headings. No `setup.sh`. Eight related-project URLs in order. The path row names the local clock. `source-photo.png` and `outline-result.png` are not text-menu captures | `tests/test_docs.py` | have |
| **TP-DOC-03** Each screenshot paragraph and alt equals the catalog cell in §2.5 | `tests/test_docs.py` | todo |

## 6. Related requirements (peer keys only)

| Key | Relationship |
|-----|----------------|
| `docs/requirements/index.md` | Registry |
| `requirement-python-project-structure` | Root `README.md` exists. Sections and pictures are this file |
| `requirement-domain-outlineimage` | Domain rows inside the user document |
| `requirement-video-ffmpeg-pipeline` | Stream copy, then re-encode. This file does not restate that procedure |
| `requirement-runtime-prerequisites` | Pip image stack. No host encoder. No root auto-install |
| `requirement-python-dependency-management` | The five pip floors in Quick Installation |
| `requirement-python-packaging` | Package name, console script, pip install |
| `requirement-python-tui` | Menu picture and the clock |
| `requirement-python-about` | The about picture. This file does not own the page |
| `requirement-python-cli-language` | Row **4** and the thirteen codes. About stays English |
| `requirement-python-cli-interface` | Product verbs the document lists. `outline` is one of them |
| `requirement-python-coding-style` | `shutil.move` for the published file |
| `requirement-class-software-dev` | Class residual |
| `README.md` | The user document |
| `screenshots/` | The captures |
| `docs/reviews/test-plan.md` | `TP-DOC-01` and `TP-DOC-03` |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-04 | Active 1.0.0 | User-document sections, Advantages, eight related projects, and twenty-two pictures. Image destinations are absolute `https`. `TP-DOC-01` have. `TP-DOC-03` todo |
| 2026-10-04 | Active 1.0.1 | About and self-management pictures match the new page. Other menu pictures still show **1.0.4**. Package string is **1.0.5** |
| 2026-10-05 | Active 1.0.2 | Quick Installation names the five pip floors. Product version stays **1.0.0** |
| 2026-10-05 | Active 1.0.3 | Public source is `https://github.com/cloudgen/OutlineImage`. Twenty captures of this program replace the previous-product pictures. Product version stays **1.0.0** |
| 2026-10-07 | Active 1.0.4 | How an outline is made explains the drawing method in plain language. Product version stays **1.0.0** |
| 2026-10-07 | Active 1.0.5 | The document's package string is **1.0.1**. Screenshot paragraphs still quote the **1.0.0** captures |
| 2026-10-10 | Active 1.0.6 | How an outline is made leaves out a brightness shadow step and a bright middle, and keeps a thin dark groove. The document's package string is **1.0.2**. Screenshot paragraphs still quote the **1.0.0** captures |

---

**Last Updated**: 2026-10-10
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
