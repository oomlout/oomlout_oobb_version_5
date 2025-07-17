import os
import sys
import difflib

def compare_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        a = f1.readlines()
        b = f2.readlines()
        if a != b:
            diff = difflib.unified_diff(a, b, fromfile=file1, tofile=file2)
            for line in diff:
                sys.stdout.write(line)
            return False
    return True

def main():
    base = 'test_good'
    current = 'test'
    ok = True
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith('.scad'):
                rel = os.path.relpath(os.path.join(root, f), base)
                f_new = os.path.join(current, rel)
                f_old = os.path.join(base, rel)
                if not os.path.exists(f_new):
                    print('Missing', f_new)
                    ok = False
                    continue
                if not compare_files(f_new, f_old):
                    ok = False
    if not ok:
        sys.exit(1)

if __name__ == '__main__':
    main()
