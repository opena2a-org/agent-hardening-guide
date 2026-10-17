"""The README sentences that list framework configuration examples may name
only frameworks that have a section in docs/configuration.md.

Run from the repository root:

    python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONFIGURATION = ROOT / "docs" / "configuration.md"


def split_names(text: str) -> list[str]:
    """Split 'A, B, and C' into ['A', 'B', 'C']."""
    return [name for name in re.split(r",\s*(?:and\s+)?|\s+and\s+", text.strip()) if name]


def configuration_sections() -> list[str]:
    """Return the level-two headings of docs/configuration.md, ignoring code blocks."""
    text = CONFIGURATION.read_text(encoding="utf-8")
    text = re.sub(r"^```.*?^```", "", text, flags=re.MULTILINE | re.DOTALL)
    return re.findall(r"^## (.+?)\s*$", text, flags=re.MULTILINE)


class FrameworkClaimsTest(unittest.TestCase):
    def assert_named_frameworks_have_sections(self, pattern: str) -> None:
        match = re.search(pattern, README.read_text(encoding="utf-8"))
        self.assertIsNotNone(match, "README sentence not found; update the pattern to its new wording")
        sections = configuration_sections()
        missing = [name for name in split_names(match.group(1)) if name not in sections]
        self.assertEqual(missing, [], "named in README.md, no section in docs/configuration.md")

    def test_intro_sentence(self):
        self.assert_named_frameworks_have_sections(
            r"includes specific configuration examples for ([^.\n]+)\."
        )

    def test_documentation_entry(self):
        self.assert_named_frameworks_have_sections(
            r"\(docs/configuration\.md\) -- ([^\n]+?) configuration examples"
        )


if __name__ == "__main__":
    unittest.main()
