# SPDX-FileCopyrightText: Copyright (c) 2022-2026 Objectionary.com
# SPDX-License-Identifier: MIT

import plistlib
import re
import sys

with open(sys.argv[1] if len(sys.argv) > 1 else 'Syntaxes/eo.tmLanguage', 'rb') as f:
    grammar = plistlib.load(f)


def scopes(line):
    found = []
    for rule in grammar['repository']['keywords']['patterns']:
        if re.search(rule['match'], line):
            found.append(rule['name'])
            break
    return found


failed = False
for line in [
    'mktemp.tmpfile.exists ++> can-create-a-temp-file',
    '1.div 0 --> stops-on-division',
    '42.eq 42 > [] +> works',
    '1.div 0 > [] -> stops',
]:
    if scopes(line) != ['keyword.operator.test.eo']:
        print('Test marker is not highlighted in: ' + line)
        failed = True
sys.exit(1 if failed else 0)
