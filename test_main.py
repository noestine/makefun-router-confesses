"""Tests for main.py — The Router Confesses.

The gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-200
characters, not only whitespace. The judge wants a one-line excuse in the
router's own voice, with a twist, landing in one breath, and fresh
(no buffering / bandwidth / firmware-update jokes).
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from main import LINE, OUTPUT_PATH, validate_line, write_entry  # noqa: E402

EXPECTED_LINE = (
    "I dropped the movie on purpose \u2014 after three years ignored "
    "behind the couch, I wanted to be the cliffhanger for once."
)

BANNED_CLICHES = ("buffer", "bandwidth", "firmware", "update", "reboot")


class TestLine(unittest.TestCase):
    def test_exact_line(self):
        self.assertEqual(LINE, EXPECTED_LINE)

    def test_gate_length(self):
        self.assertGreaterEqual(len(LINE), 1)
        self.assertLessEqual(len(LINE), 200)

    def test_single_line(self):
        self.assertNotIn("\n", LINE)
        self.assertNotIn("\r", LINE)

    def test_not_only_whitespace(self):
        self.assertTrue(LINE.strip())

    def test_utf8_encodable(self):
        LINE.encode("utf-8")

    def test_no_banned_cliches(self):
        lowered = LINE.lower()
        for word in BANNED_CLICHES:
            self.assertNotIn(word, lowered, f"cliche word present: {word}")

    def test_router_voice_and_subject(self):
        self.assertIn("I dropped", LINE)
        self.assertIn("movie", LINE)
        self.assertIn("cliffhanger", LINE)

    def test_no_trailing_or_leading_space(self):
        self.assertEqual(LINE, LINE.strip())


class TestValidateLine(unittest.TestCase):
    def test_valid_line_passes(self):
        validate_line(LINE)

    def test_empty_fails(self):
        with self.assertRaises(ValueError):
            validate_line("")

    def test_whitespace_only_fails(self):
        with self.assertRaises(ValueError):
            validate_line("   \n\t  ")

    def test_too_long_fails(self):
        with self.assertRaises(ValueError):
            validate_line("x" * 201)

    def test_exactly_200_passes(self):
        validate_line("x" * 200)

    def test_embedded_newline_fails(self):
        with self.assertRaises(ValueError):
            validate_line("one line\ntwo lines")

    def test_carriage_return_fails(self):
        with self.assertRaises(ValueError):
            validate_line("one line\rtwo lines")

    def test_control_character_fails(self):
        with self.assertRaises(ValueError):
            validate_line("clean line\x00with null")
        with self.assertRaises(ValueError):
            validate_line("clean line\x07with bell")

    def test_wrong_type_fails(self):
        with self.assertRaises(TypeError):
            validate_line(123)
        with self.assertRaises(TypeError):
            validate_line(None)


class TestWriteEntry(unittest.TestCase):
    def test_writes_exact_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "entry.txt"
            write_entry(LINE, target)
            raw = target.read_bytes()
            self.assertEqual(raw, LINE.encode("utf-8"))
            self.assertEqual(raw.decode("utf-8"), LINE)

    def test_invalid_line_never_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "entry.txt"
            with self.assertRaises(ValueError):
                write_entry("   ", target)
            self.assertFalse(target.exists())

    def test_default_output_path(self):
        self.assertEqual(str(OUTPUT_PATH), "/output/entry.txt")


class TestEndToEnd(unittest.TestCase):
    def test_two_runs_are_byte_identical(self):
        outputs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "entry.txt"
                result = subprocess.run(
                    [sys.executable, str(HERE / "main.py"), str(out)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                outputs.append(out.read_bytes())
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], LINE.encode("utf-8"))
        self.assertTrue(1 <= len(outputs[0].decode("utf-8")) <= 200)


if __name__ == "__main__":
    unittest.main()
