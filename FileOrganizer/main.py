
from pathlib import Path
import shutil
import time

folder = Path(__file__).parent / "TestFiles"
file_types = {
    "Images":
		[
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp", ".svg", ".ico"
		],
    "Documents":
		[
        ".pdf", ".doc", ".docx", ".txt",
        ".rtf", ".odt", ".xls", ".xlsx",
        ".ppt", ".pptx", ".csv"
		],
    "Music": [".mp3", ".wav", ".ogg", ".flac",".m4a", ".wma", ".aac"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov",".wmv", ".webm", ".mpeg", ".mpg"],
    "Archives": [".zip", ".rar", ".7z", ".tar",".gz", ".bz2"],
    "Programming": [".py", ".cpp", ".h", ".cs",".js", ".html",
					".css", ".json",".sql", ".java", ".php"],
    "Programs": [".exe", ".msi", ".bat", ".cmd"]
}

def sort_file(file):
    print(f"Початкова назва файлу: {file.name}")
    suffix = file.suffix.lower()
    destination_name = "Other"
    for category, extensions in file_types.items():
        if suffix in extensions:
            destination_name = category
            break
    destination = folder / destination_name
    destination.mkdir(exist_ok=True)
    target = destination / file.name
    counter = 1
    while target.exists():
        target = (destination /
		(
			f"{file.stem}_{counter}{file.suffix}")
		)
        counter += 1
    try:
        shutil.move(str(file), str(target))
        print(f"Початкова назва: {file.name}")
        print(f"Повний шлях призначення: {target}")
        print(f"Назва після переміщення: {target.name}")
    except (OSError, shutil.Error) as error:
        print(f"Помилка переміщення {file.name}: {error}")

def main():
    if not folder.exists():
        print(f"Папку не знайдено: {folder}")
        return
    print("Початкове сортування файлів...")
    for file in list(folder.iterdir()):
        if file.is_file():
            sort_file(file)
    print("\nFileOrganizer працює!")
    print(f"Стежимо за папкою: {folder}")
    print("Для зупинки натисни Ctrl+C.\n")
    pending = {}
    try:
        while True:
            for file in list(folder.iterdir()):
                if not file.is_file():
                    continue
                try:
                    stat = file.stat()
                    signature = \
					(
                        stat.st_size,
                        stat.st_mtime_ns
                    )
                    if file not in pending:
                        pending[file] = signature
                    elif pending[file] == signature:
                        pending.pop(file, None)
                        sort_file(file)
                    else:
                        pending[file] = signature
                except FileNotFoundError:
                    pending.pop(file, None)
            for file in list(pending):
                if not file.exists():
                    pending.pop(file, None)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nFileOrganizer зупинено.")
if __name__ == "__main__":
    main()




