import os
from pathlib import Path

def safe_delete(file_path: Path):
    """Geçici dosyayı sil"""
    try:
        if file_path.exists():
            os.unlink(file_path)
    except Exception:
        pass
