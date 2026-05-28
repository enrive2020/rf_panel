from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

DATA_DIR = APP_DIR / "data"
TEMP_DIR = APP_DIR / "temp"
EXPORTS_DIR = APP_DIR / "exports"
LOGS_DIR = APP_DIR / "logs"

DB_PATH = DATA_DIR / "rf_panel.db"

CLIENT_PATH = r"D:\RF-Platform\Client"


def ensure_runtime_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)