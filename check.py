#!/usr/bin/python3

from PyInquirer import prompt, print_json
import os
import os.path as path
import sys
from operator import itemgetter
from collections import defaultdict

langs = {
    'py': {
        'name': 'Python 3',
        'ext': 'py',
        'command': 'python3'
    },
    'c++': {
        'name': 'C++',
        'ext': 'cpp',
        'command': 'z++'
    }
}

pwd = os.getcwd()

test_case_dir = path.join(pwd, 'test-cases')
if not path.isdir(test_case_dir):
    print('`test-case` directory not found', file=sys.stderr)
    sys.exit(1)
test_cases = []
suites = defaultdict(set)
for filename in os.listdir(test_case_dir):
    name, ext = filename.split('.')
    suites[name].add(ext)
for name, exts in suites.items():
    if 'in' not in exts:
        print(f'Error: test suite `{name}` does not have input file', file=sys.stderr)
        continue
    test_cases.append((name, 'ans' in exts))
test_cases.sort(key=itemgetter(0))

test_suite = None
if len(test_cases) == 0:
    print('Error: no test suites found', file=sys.stderr)
    sys.exit(1)
elif len(test_cases) == 1:
    test_suite = test_cases[0][0]
else:
    questions = [
        {
            'type': 'list',
            'name': 'test-case',
            'message': 'Choose a test suite:',
            'choices': [f'{name} {"(no answer file)" if not ans_present else ""}' for name, ans_present in test_cases]
        }
    ]
    answers = prompt(questions)
    test_suite = answers['test-case']

problem_name = path.basename(pwd)

detected_langs = []
for lang in langs.keys():
    if path.isfile(path.join(pwd, f'{problem_name}.{langs[lang]["ext"]}')):
        detected_langs.append(lang)

chosen_lang = None
if len(detected_langs) == 0:
    print('Error: no solution file found', file=sys.stderr)
    sys.exit(1)
elif len(detected_langs) == 1:
    chosen_lang = detected_langs[0]
else:
    questions = [
        {
            'type': 'list',
            'name': 'lang',
            'message': 'Choose a language:',
            'choices': [langs[lang]['name'] for lang in langs.keys()]
        }
    ]
    answers = prompt(questions)
    chosen_lang = answers['lang']
