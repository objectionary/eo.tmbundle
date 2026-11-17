"""Regression coverage for binding operators in the EO keyword rules."""

from pathlib import Path
import plistlib
import re
import unittest


class AutoNameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        grammar = Path(__file__).resolve().parents[1] / "Syntaxes/eo.tmLanguage"
        with grammar.open("rb") as source:
            cls.rules = plistlib.load(source)["repository"]["keywords"]["patterns"]

    def assert_operator(self, line, token, scope):
        start = line.index(token)
        end = start + len(token)
        matches = [
            (match.group().strip(), rule["name"])
            for rule in self.rules
            for match in re.finditer(rule["match"], line)
            if match.start() < end and match.end() > start
        ]
        self.assertEqual([(token, scope)], matches)

    def test_auto_name_suffixes(self):
        for line in (
            'getenv "TMP" empty >> tmp',
            'getenv "TMP" empty >> tmp!',
            "[] >>",
            "[] >>!",
            "[] >>\n",
            "[] >>!\n",
        ):
            with self.subTest(line=line):
                self.assert_operator(line, ">>", "keyword.operator.bound.eo")

    def test_constant_suffix_keeps_its_scope(self):
        self.assert_operator("[] >>!", "!", "keyword.operator.constant.eo")

    def test_existing_binding_and_test_operators(self):
        self.assert_operator("42 > x", ">", "keyword.operator.bound.eo")
        self.assert_operator("[] +> test", "+>", "keyword.operator.test.eo")


if __name__ == "__main__":
    unittest.main()
