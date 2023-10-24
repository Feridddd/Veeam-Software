import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("--interval", type=int, default=60, help="Synchronization interval in seconds (default: 1 min)")
    parser.add_argument("--log_file", default="logs/sync.log", help="Log file path (default: logs folder and sync.log)")

    args = parser.parse_args()


