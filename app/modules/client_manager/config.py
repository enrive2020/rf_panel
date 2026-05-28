from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = APP_DIR / "data"

DB_PATH = DATA_DIR / "rf_panel.db"

CLIENT_PATH = r"D:\RF-Platform\Client"

def ensure_data_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)