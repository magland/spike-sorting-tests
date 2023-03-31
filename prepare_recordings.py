# execute_sortings.py
from core.load_config import load_config
from core.prepare_single_recording import prepare_single_recording


def main():
    config = load_config()
    
    for recording in config.recordings:
        print(f"Preparing recording: {recording.id}")
        prepare_single_recording(config, recording)
        print('')

if __name__ == '__main__':
    main()