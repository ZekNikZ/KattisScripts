#!/usr/local/bin/python3

from PyInquirer import prompt
import click
import os
import os.path as path
import sys
from operator import itemgetter
from collections import defaultdict
import subprocess

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

# TODO: improve documentation
@click.command()
@click.option('-l', '--lang', default='py', help='language of submission file')
@click.argument('test', default='')
def main(lang, test):
    """
    This script will run a test suite against your submission file.

    If your program generates correct output, nothing will be printed and exit code 0 will be returned.
    If your program generates incorrect output, an interactive diff will be openend and exit code 1 will be returned.
    If your program has a run-time error, exit code 43 will be returned and the contents of STDERR will be printed.

    By default, this script will search for a submission file in the working directory and a test case file in the test-case/ directory.
    If there are multiple submission files or multiple test suites, an interactive prompt will be launched to select which one(s) to run.
    This behavior can be overrided by passing the indicated command-line arugments above.
    """
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

    chosen_test_suite = None
    if len(test_cases) == 0:
        print('Error: no test suites found', file=sys.stderr)
        sys.exit(1)
    elif len(test_cases) == 1:
        chosen_test_suite = test_cases[0][0]
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
        chosen_test_suite = answers['test-case']

    problem_name = path.basename(pwd)

    detected_langs = []
    for l in langs.keys():
        if path.isfile(path.join(pwd, f'{problem_name}.{langs[l]["ext"]}')):
            detected_langs.append(l)

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

    submission_file_path= path.join(pwd, f'{problem_name}.{chosen_lang}')
    input_file_path = path.join(pwd, 'test-cases', f'{chosen_test_suite}.in')
    answer_file_path = path.join(pwd, 'test-cases', f'{chosen_test_suite}.ans')
    with open(input_file_path) as input_file:
        # Submission
        submission_proc = subprocess.run(
            [
                langs[chosen_lang]['command'],
                submission_file_path
            ],
            stdin=input_file,
            stdout=subprocess.PIPE
        )

        # Diff
        if path.isfile(answer_file_path):
            diff_proc = subprocess.run(
                [
                    'diff',
                    '--unified=5',
                    answer_file_path,
                    '-'
                ],
                input = submission_proc.stdout,
                stdout=subprocess.PIPE
            )
            ydiff_proc = subprocess.run(
                [
                    'ydiff',
                    '-s',
                    '--wrap'
                ],
                input=diff_proc.stdout
            )
            sys.exit(diff_proc.returncode)
        else:
            sys.exit(43)

if __name__ == '__main__':
    main()