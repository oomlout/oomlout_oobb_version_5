import os
import sys
import difflib

def compare_files(file1, file2, report_file):
    with open(file1) as f1, open(file2) as f2:
        a = f1.readlines()
        b = f2.readlines()
        if a != b:
            diff = difflib.unified_diff(a, b, fromfile=file1, tofile=file2)
            with open(report_file, 'a') as report:
                report.write(f'Differences in {file1} vs {file2}:\n')
                report.writelines(diff)
                report.write('\n')
            return False
    return True

def main():
    base = 'test_good'
    current = 'test'
    report_file = 'report.txt'
    ok = True

    # Overwrite or create the report file
    with open(report_file, 'w') as report:
        report.write('Comparison Report\n')
        report.write('=================\n\n')

    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith('.scad'):
                rel = os.path.relpath(os.path.join(root, f), base)
                f_new = os.path.join(current, rel)
                f_old = os.path.join(base, rel)
                if not os.path.exists(f_new):
                    with open(report_file, 'a') as report:
                        report.write(f'Missing file: {f_new}\n')
                    ok = False
                    continue
                if not compare_files(f_new, f_old, report_file):
                    ok = False

    if not ok:
        with open(report_file, 'a') as report:
            report.write('\nComparison failed.\n')
            #sys.exit(1)
    else:
        with open(report_file, 'a') as report:
            report.write('\nAll files match.\n')
        print('All files match.')

if __name__ == '__main__':
    main()