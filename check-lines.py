#! python3

# How to use:
# ./check-lines.py ./gameplay/**/*.py ./resources/**/*.py ./main.py

import sys

args = list(sys.argv)[1:]

r = 0
if len(args) == 0:
    print("Filenames not detected.")
    exit(0)

i = 0
while i < len(args):
    try:
        open(args[i], 'r', encoding='utf-8')
    except Exception:
        print(f"File '{args[i]}' not found.")
        print('Trying to continue anyway...')
        del args[i]

    try:
        with open(args[i], 'r', encoding='utf-8') as f:
            ln = 0
            lines = f.read().splitlines()
            for s in lines:
                if s.strip() != "" and s.strip()[0] != '#':
                    ln += 1
            r += ln
            print(f"File {args[i]}: {ln} lines.")

    except IsADirectoryError:
        print("A folder was skipped.")
    i += 1

print(r)
