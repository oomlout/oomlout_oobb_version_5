import os
import shutil

def main():
    if os.path.exists('test_good'):
        shutil.rmtree('test_good')
    if os.path.exists('test'):
        shutil.copytree('test', 'test_good')

if __name__ == '__main__':
    main()
