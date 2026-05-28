from client_scanner import ClientScanner
from storage import Storage


CLIENT_PATH = r"D:\RF-Platform\Client"



def size_mb(value):
    return value / 1024 / 1024


def main():
    scanner = ClientScanner(CLIENT_PATH)
    storage = Storage("scan.db")

    report = scanner.scan()
    session_id = storage.save_scan(report)

    print("Сканирование завершено")
    print(f"Session ID: {session_id}")
    print(f"Client: {report['client_path']}")
    print(f"Files: {report['total_files']}")
    print(f"Folders: {report['total_folders']}")
    print(f"Size: {size_mb(report['total_size_bytes']):.2f} MB")


if __name__ == "__main__":
    main()