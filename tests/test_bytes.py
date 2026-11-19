# SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
# SPDX-License-Identifier: MIT

"""Regression coverage for EO bytes and number rules; run with unittest discovery."""
import plistlib
import re
import unittest
from pathlib import Path


class BytesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        grammar = Path(__file__).resolve().parents[1] / 'Syntaxes' / 'eo.tmLanguage'
        with grammar.open('rb') as source:
            cls.rules = plistlib.load(source)['repository']['constants']['patterns']

    def tokens(self, line):
        """Scan like TextMate: leftmost match wins, the earlier rule breaks ties."""
        found = []
        pos = 0
        while pos <= len(line):
            best = None
            for rule in self.rules:
                match = re.compile(rule['match']).search(line, pos)
                if match and match.end() > match.start() and (
                        best is None or match.start() < best[0].start()):
                    best = (match, rule['name'])
            if best is None:
                break
            found.append((best[0].group(), best[1].replace('(?<![\\w-])', '')))
            pos = best[0].end()
        return found

    def test_bytes(self):
        for line, text in (
            ('01-02-03 > @', '01-02-03'),
            ('FF- > @', 'FF-'),
            ('00- > @', '00-'),
            ('-- > @', '--'),
            ('42-43 > @', '42-43'),
            ('42- > @', '42-'),
            ('AB-CD- > @', 'AB-CD-'),
        ):
            with self.subTest(line=line):
                self.assertEqual([(text, 'constant.numeric.bytes.eo')], self.tokens(line))

    def test_integers(self):
        for line, text in (('42 > @', '42'), ('-7 > @', '-7'), ('0 > @', '0')):
            with self.subTest(line=line):
                self.assertEqual([(text, 'constant.numeric.int.eo')], self.tokens(line))


if __name__ == '__main__':
    unittest.main()
