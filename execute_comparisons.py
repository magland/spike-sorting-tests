# execute_sortings.py
import argparse
from core.execute_single_comparison import execute_single_comparison
from core.load_config import load_config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Execute spike sorting tests.")
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = load_config()
    
    for sorting in config.sortings:
        for sorting2 in config.sortings:
            if sorting2.recording == sorting.recording and sorting2.sorter != sorting.sorter:
                print(f"Running comparison for {sorting.recording} of {sorting.sorter}/{sorting2.sorter}")
                execute_single_comparison(config, sorting, sorting2)
                print('')

if __name__ == '__main__':
    main()