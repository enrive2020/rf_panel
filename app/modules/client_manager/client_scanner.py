import os
from pathlib import Path
from datetime import datetime

from rules import CATEGORY_RULES, IGNORED_DIRS


def fmt_time(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def detect_category(relative_path):
    if relative_path == ".":
        return "root"

    top = relative_path.split("\\")[0].split("/")[0]

    return CATEGORY_RULES.get(top, "unknown")


class ClientScanner:
    def __init__(self, client_path):
        self.client_path = Path(client_path)

    def scan(self):
        if not self.client_path.exists():
            raise FileNotFoundError(f"Client path not found: {self.client_path}")

        folders = {}
        files = []

        total_size = 0

        for dirpath, dirnames, filenames in os.walk(self.client_path):
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

            current = Path(dirpath)
            rel_dir = str(current.relative_to(self.client_path)) if current != self.client_path else "."
            category = detect_category(rel_dir)

            folder_info = folders.setdefault(rel_dir, {
                "path": rel_dir,
                "category": category,
                "files_count": 0,
                "total_size_bytes": 0,
                "last_modified_ts": None,
                "last_modified": None,
                "extensions": {},
            })

            for filename in filenames:
                file_path = current / filename

                try:
                    stat = file_path.stat()
                except OSError:
                    continue

                ext = file_path.suffix.lower() or "[no_ext]"
                rel_file = str(file_path.relative_to(self.client_path))

                folder_info["files_count"] += 1
                folder_info["total_size_bytes"] += stat.st_size
                folder_info["extensions"][ext] = folder_info["extensions"].get(ext, 0) + 1

                total_size += stat.st_size

                if folder_info["last_modified_ts"] is None or stat.st_mtime > folder_info["last_modified_ts"]:
                    folder_info["last_modified_ts"] = stat.st_mtime
                    folder_info["last_modified"] = fmt_time(stat.st_mtime)

                files.append({
                    "path": rel_file,
                    "folder": rel_dir,
                    "name": filename,
                    "extension": ext,
                    "size_bytes": stat.st_size,
                    "modified_at": fmt_time(stat.st_mtime),
                    "category": category,
                })

        clean_folders = []

        for folder in folders.values():
            folder.pop("last_modified_ts", None)
            clean_folders.append(folder)

        return {
            "client_path": str(self.client_path),
            "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_files": len(files),
            "total_folders": len(clean_folders),
            "total_size_bytes": total_size,
            "folders": sorted(clean_folders, key=lambda x: x["path"]),
            "files": files,
        }