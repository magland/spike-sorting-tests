import os
import shutil


def main():
    if not os.path.exists('output'):
        os.mkdir('output')
    shutil.copyfile('spike_sorting_config.yaml', 'output/spike_sorting_config.yaml')

if __name__ == '__main__':
    main()