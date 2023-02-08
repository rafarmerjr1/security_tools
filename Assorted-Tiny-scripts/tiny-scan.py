#simple bandit wrapper as a POC for larger SAST wrapper project

import subprocess
import os
import sys
import time
import argparse


def check_for_scanner(scanner):
    which_scanner = subprocess.Popen(['which', scanner], stdout=subprocess.PIPE)
    which_scanner.wait(timeout=2)
    scanner_path = which_scanner.stdout.read().decode('utf-8').strip()
    print(scanner_path)
    return scanner_path


def run_scan(scanlist):
    resultsfile = write_results(scanlist[-1])
    print(resultsfile)
    f = open(resultsfile, 'w')
    run_scan = subprocess.Popen(scanlist, stdout=f)
    run_scan.wait(timeout=15)
    print(f'\nResults written to {resultsfile}')


def write_results(filename):
    epoch = int(time.time())
    if filename in [ '.', './']:
        filename = os.getcwd().split("/")[-1:]
    if filename.count("/") > 1:
        print(filename)
        filename = filename.split("/")
        filename = filename[-1]
    else:
        filename = filename[0]
    outfile = f'{filename}-{epoch}.txt'
    return outfile

### Only used if called directly:

def parse_args():
    parser = argparse.ArgumentParser(
        description="TinyPy SAST - Tiny Static Application Security Testing"
    )
    group = parser.add_mutually_exclusive_group()


    group.add_argument(
        '-f',
        '--filename', 
        help="Specifies that a single file should be scan.  Filename should follow." 
    )

    group.add_argument(
        '-d',
        '--directory',
        help="Specifies that a directory should be scanned.  Directory name should follow."
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    
    if len(sys.argv) < 2:
        print("No arguments found.  Please try again. Use '-h' for help.")

    else:
        scanner_path = check_for_scanner('bandit')

        if args.filename:
            if '..' in args.filename:
                sys.exit("Only full paths or current directory may be scanned, not '../")
            filename = args.filename

            scanlist = [scanner_path, filename]
        elif args.directory:
            if '..' in args.directory:
                sys.exit("Only full paths or current directory may be scanned, not '../")
            directory = args.directory
            scanlist = [scanner_path, '-r', directory]

        run_scan(scanlist)
 