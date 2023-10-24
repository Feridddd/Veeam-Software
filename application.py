import argparse
import logging
import os
import shutil
import time


def setup_logging(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler for the log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Create a console handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def copy_files(source_file, replica_file):
    if not os.path.exists(replica_file):
        shutil.copy2(source_file, replica_file)
        logging.info(f"File created: {source_file} -> {replica_file}")
    elif os.path.getmtime(source_file) > os.path.getmtime(replica_file):
        shutil.copy2(source_file, replica_file)
        logging.info(f"File updated: {source_file} -> {replica_file}")


def remove_extra_files(replica_folder, source_folder):
    for root, _, files in os.walk(replica_folder):
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_folder, os.path.relpath(replica_file, replica_folder))

            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"File removed: {replica_file}")


def synchronize_folders(source_folder, replica_folder, interval, log_file):
    setup_logging(log_file)

    while True:
        for root, _, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)

            if not os.path.exists(replica_path):
                os.makedirs(replica_path)

            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_path, file)

                copy_files(source_file, replica_file)

        remove_extra_files(replica_folder, source_folder)

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=60, help="Synchronization interval in seconds (default: 1 min)")
    parser.add_argument("--log_file", default="logs/sync.log", help="Log file path (default: logs folder and sync.log)")

    args = parser.parse_args()

    synchronize_folders(args.source_folder, args.replica_folder, args.interval, args.log_file)
