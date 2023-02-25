
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Stocker: A stock market prediction tool using deep learning.")
    parser.add_argument("--project-name", type=str, default="Stocker", help="Project name (default: Stocker).")
    parser.add_argument("--log-level", type=str, default="DEBUG", help="Log level (default: DEBUG).")
    parser.add_argument("--log-file", type=str, default="Stocker.log", help="Output Log filename (default: Stocker.log).")
    parser.add_argument("--log-dir", type=str, default="Data/Logs", help="Output Log directory (default: Data/Logs).")
    parser.add_argument("--enable-datetime-stamp", action="store_true", default=True, help="Enables datetime stamp in log filename (default: True).")
    parser.add_argument("--verbose", action="store_true", default=False, help="Enables terminal logging utilities (default: False).")
    args = parser.parse_args()
    return args
