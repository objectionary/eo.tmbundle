"""Regression coverage for EO keyword rules; run with unittest discovery."""
import plistlib
import re
import unittest
from pathlib import Path


class MissingTokensTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        grammar = Path(__file__).resolve().parents[1] / 'Syntaxes' / 'eo.tmLanguage'
        with grammar.open('rb') as source:
            cls.rules = plistlib.load(source)['repository']['keywords']['patterns']

    def matches(self, line, scope):
        return [
            match.group()
            for rule in self.rules
            if rule['name'] == scope
            for match in re.finditer(rule['match'], line)
        ]

    def test_tuple_marker(self):
        for line in ('* 1 2 3 > @', 'win32 *1'):
            with self.subTest(line=line):
                self.assertEqual(['*'], self.matches(line, 'keyword.operator.tuple.eo'))

    def test_signature(self):
        for line in ('[] > div /Q.number', '? > x /Q.number'):
            with self.subTest(line=line):
                self.assertEqual(['/'], self.matches(line, 'keyword.operator.signature.eo'))

    def test_terminator(self):
        self.assertEqual(['T'], self.matches('T "Cant delete the file"',
                                            'keyword.control.terminator.eo'))

    def test_identity(self):
        self.assertEqual(['I'], self.matches('mktemp.tmpfile.deleted.open "r" I "recovered"',
                                            'keyword.control.identity.eo'))

    def test_letter_boundaries(self):
        for scope in ('keyword.control.terminator.eo', 'keyword.control.identity.eo'):
            with self.subTest(scope=scope):
                self.assertEqual([], self.matches('title if TI IT T1 I1 _T _I', scope))

    def test_pipe_at_start_of_line(self):
        for indent in ('', '  ', '\t'):
            with self.subTest(indent=indent):
                self.assertEqual([indent + '|'], self.matches(indent + '| foo',
                                                             'keyword.operator.pipe.eo'))

    def test_inline_pipe_is_not_a_pipe_line(self):
        self.assertEqual([], self.matches('foo | bar', 'keyword.operator.pipe.eo'))


if __name__ == '__main__':
    unittest.main()
