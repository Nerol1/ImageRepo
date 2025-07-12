from pathlib import Path
import uuid


ALLOWED_EXTENSIONS = ['.png', '.jpeg', '.jpg', '.gif']
MAX_FILE_SIZE = 5*1024*10124

def is_allowed_file(filename: Path) -> bool:
    """Проверяем, есть ли расширение в списке разрешенных."""
    ext = filename.suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def get_unique_name(filename: Path) -> str:
    ext = filename.suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    print(f"Новое имя файла {unique_name}")
    return unique_name
