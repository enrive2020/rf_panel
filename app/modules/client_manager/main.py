from app.config import CLIENT_PATH, DB_PATH, ensure_runtime_dirs
from app.modules.client_manager.client_scanner import ClientScanner
from app.modules.client_manager.storage import Storage


def size_mb(value):
    return value / 1024 / 1024


def main():
    ensure_runtime_dirs()

    scanner = ClientScanner(CLIENT_PATH)
    storage = Storage(DB_PATH)

    report = scanner.scan()
    session_id = storage.save_scan(report)

    print("Сканирование завершено")
    print(f"Session ID: {session_id}")
    print(f"Database: {DB_PATH}")
    print(f"Client: {report['client_path']}")
    print(f"Files: {report['total_files']}")
    print(f"Folders: {report['total_folders']}")
    print(f"Size: {size_mb(report['total_size_bytes']):.2f} MB")


if __name__ == "__main__":
    main()