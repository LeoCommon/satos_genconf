import argparse
from .genconf import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file')
    parser.add_argument('--template', default='templates/rauc-hawkbit-updater.ini.j2')
    parser.add_argument('-o', '--output-file', default='rauc-hawkbit-updater.ini')
    parser.add_argument('--mock-run', default=False)
    return parser.parse_args()
    
def main():
    args = parse_args()
    run(args)

if __name__ == '__main__':
    main()