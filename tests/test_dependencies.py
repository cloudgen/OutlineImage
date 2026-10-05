# TP-DEP-01..04 — pip strings. Primary law: requirement-python-dependency-management.
# Does not import rembg, cv2, or Pillow.
import re
import unittest
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = (
    "ChronicleLogger>=1.3.1",
    "numpy>=2.3.0",
    "Pillow>=12.1.0",
    "opencv-python-headless>=5.0.0.93",
    "rembg>=2.0.85",
)
GUI_WHEEL = "opencv-python"


def _manifest_dependencies():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r"(?ms)^dependencies = \[(.*?)^\]", text)
    if match is None:
        return []
    return re.findall(r'"([^"]+)"', match.group(1))


def _numeric_tuple(text):
    parts = []
    for bit in text.split("."):
        digits = ""
        for char in bit:
            if char.isdigit():
                digits += char
            else:
                break
        if digits == "":
            break
        parts.append(int(digits))
    return tuple(parts)


class DependencyTests(unittest.TestCase):
    def test_every_entry_has_a_specifier(self):
        found = _manifest_dependencies()
        self.assertEqual(list(SPECS), found)
        for entry in found:
            self.assertRegex(entry, r"(==|>=|~=|!=|<=|<|>)")

    def test_gui_wheel_is_absent(self):
        names = [entry.split(">=")[0].split("==")[0] for entry in _manifest_dependencies()]
        self.assertIn("opencv-python-headless", names)
        self.assertNotIn(GUI_WHEEL, names)

    def test_requirement_matches_the_manifest(self):
        law = (
            ROOT / "docs" / "requirements" / "requirement-python-dependency-management.md"
        ).read_text(encoding="utf-8")
        for spec in SPECS:
            self.assertIn(spec, law)
        self.assertIn("`opencv-python` is not declared", law)
        self.assertNotIn("requirements.txt", (ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    def test_installed_wheels_meet_floors_when_present(self):
        for spec in SPECS:
            name, floor = spec.split(">=", 1)
            try:
                installed = version(name)
            except PackageNotFoundError:
                continue
            self.assertGreaterEqual(_numeric_tuple(installed), _numeric_tuple(floor))
