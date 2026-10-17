"""The README License section must name the license that the LICENSE file
contains, name no other license listed in LICENSE_HEADERS, and link to the
LICENSE file.

Run from the repository root:

    python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
LICENSE = ROOT / "LICENSE"

# Opening words of a license text, mapped to the license's SPDX identifier.
LICENSE_HEADERS = {
    "Apache License Version 2.0,": "Apache-2.0",
    "MIT License": "MIT",
}


def mentions(identifier: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(identifier)}\b", text) is not None


class LicenseStatementTest(unittest.TestCase):
    def license_identifier(self) -> str:
        opening = " ".join(LICENSE.read_text(encoding="utf-8").split())
        found = [spdx for header, spdx in LICENSE_HEADERS.items() if opening.startswith(header)]
        self.assertEqual(len(found), 1, "LICENSE does not open with a header listed in LICENSE_HEADERS")
        return found[0]

    def license_section(self) -> str:
        text = README.read_text(encoding="utf-8")
        text = re.sub(r"^```.*?^```", "", text, flags=re.MULTILINE | re.DOTALL)
        match = re.search(r"^## License[ \t]*$(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, "README.md has no '## License' section")
        return match.group(1)

    def test_names_the_license_in_license_file(self):
        identifier = self.license_identifier()
        self.assertTrue(mentions(identifier, self.license_section()), f"README License section does not name {identifier}")

    def test_names_no_other_listed_license(self):
        identifier = self.license_identifier()
        section = self.license_section()
        others = [spdx for spdx in LICENSE_HEADERS.values() if spdx != identifier and mentions(spdx, section)]
        self.assertEqual(others, [], "README License section names a license that LICENSE does not contain")

    def test_links_to_license_file(self):
        self.assertRegex(self.license_section(), r"\]\(LICENSE\)", "README License section does not link to LICENSE")


if __name__ == "__main__":
    unittest.main()
