# execute_sortings.py
import argparse
from core.execute_single_sorting import execute_single_sorting
from core.load_config import load_config


def parse_arguments():
    parser = argparse.ArgumentParser(description="Execute spike sorting tests.")
    parser.add_argument('--sorter', type=str, help='Filter sortings to only those that use the specified sorter ID')
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = load_config()
    
    filtered_sortings = config.sortings
    
    if args.sorter:
        filtered_sortings = [sorting for sorting in config.sortings if sorting.sorter == args.sorter]

    for sorting in filtered_sortings:
        print(f"Running spike sorting for {sorting.recording} using {sorting.sorter}")
        execute_single_sorting(config, sorting)
        print('')

if __name__ == '__main__':
    main()