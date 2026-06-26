from pathlib import Path


# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SQLite Database Path
DATABASE_URL = f"sqlite:///{BASE_DIR / 'myntra.db'}"

# Myntra Base URL
MYNTRA_BASE_URL = "https://www.myntra.com"

# Request Timeout (seconds)
REQUEST_TIMEOUT = 30

# Request Headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}