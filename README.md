# KattisScripts

This is a collection of my scripts that aid in Kattis submissions and setups. 
To add them to your `PATH`, you can add `PATH="$PATH:/path/to/this/repo` to your `.bashrc` 
or use the `set -U fish_user_paths /path/to/this/repo $fish_user_paths` command in the `fish` shell.

## Languages

These scripts currently support the following languages:

* Python 3
* C++

## Setup

This collection requires the following third-party utilities:
* `curl` 
* `kattis` ([Kattis CLI](https://github.com/Kattis/kattis-cli))
* `ydiff` [GitHub Repo](https://github.com/ymattw/ydiff)

## Scripts

1. [`kget`](#kget) - download problem(s) test cases
2. [`kup`](#kup) - upload solution(s) to problem
3. [`check`](#check) - check solution against a test case
4. [`z++`](#z++) - a wrapper to compile and run a C++ program in one command

### `kget`

Usage: `kget <problem-id> [problem-id...]`

This command creates folders with test cases for the specified problem IDs. Example:

```
kget signprofile howmanydigits color

Creates this folder struture:
./
  signprofile/
    test-cases/
      sample.in
      sample.ans
    signprofile.py
  howmanydigits/
    test-cases/
      sample.in
      sample.ans
    howmanydigits.py
  color/
    test-cases/
      sample01.in
      sample01.ans
      sample02.in
      sample02.ans
    color.py
```

If you want to change the default file, edit the script on the third-to-last line.

### `kup`

Usage: `kup [lang] [lang...]`

This command uploads solution(s) to a problem. 
The problem is determined by the name of the folder that you are in (`./`).
It looks for files with the same name, and attempts to upload those.

Examples:

```
Folder structure:
signprofile/
  signprofile.py

cd signprofile
kup

==> uploads signprofile.py
```

```
Folder structure:
signprofile/
  signprofile.py
  signprofile.cpp

cd signprofile
kup cpp

==> uploads signprofile.cpp
```

### `check`

Usage: `check [lang] <test-case-id>`

Runs a diff of output against `<test-case-id>.ans` using `<test-case-id>.in` as STDIN.

### `z++`

Usage: `z++ <file.cpp>`

Compiles and runs `<file.cpp>`.
