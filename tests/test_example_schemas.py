"""A "$schema" key in an example JSON file that points into this repository
must name a file that exists in the repository.

Run from the repository root:

    python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
REPOSITORY_RAW_PREFIX = "https://raw.githubusercontent.com/opena2a-org/agent-hardening-guide/main/"


def schema_references() -> list[tuple[str, str]]:
    """Return (example file, $schema value) for each example that declares one."""
    references = []
    for path in sorted(EXAMPLES.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "$schema" in data:
            references.append((path.name, data["$schema"]))
    return references


class ExampleSchemasTest(unittest.TestCase):
    def test_repository_schemas_exist(self):
        missing = [
            (name, url)
            for name, url in schema_references()
            if url.startswith(REPOSITORY_RAW_PREFIX)
            and not (ROOT / url[len(REPOSITORY_RAW_PREFIX):]).is_file()
        ]
        self.assertEqual(missing, [], "$schema points at a file this repository does not contain")


if __name__ == "__main__":
    unittest.main()
