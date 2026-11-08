import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
source_dir = r"E:\downloads"

# Where files should go (inside the source_dir)
dest_dirs = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Code": [".py", ".js", ".html", ".css", ".json"]
}

# Chrome/Edge/Firefox use temporary extensions while a download is in progress.
TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp"}

class MoverHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            self.process_folder()

    def on_modified(self, event):
        if not event.is_directory:
            self.process_folder()

    def on_moved(self, event):
        if not event.is_directory:
            self.process_folder()

    def process_folder(self):
        try:
            with os.scandir(source_dir) as entries:
                for entry in entries:
                    self.move_file(entry)
        except Exception as e:
            print(f"Folder scan error: {e}")

    def wait_until_stable(self, path, checks=2, interval=1):
        """Wait until the file size stays unchanged for consecutive checks."""
        try:
            previous_size = os.path.getsize(path)

            for _ in range(checks):
                time.sleep(interval)

                if not os.path.exists(path):
                    return False

                current_size = os.path.getsize(path)

                if current_size != previous_size:
                    previous_size = current_size
                    continue

            return True

        except (FileNotFoundError, PermissionError, OSError):
            return False

    def move_file(self, entry):
        # Ignore directories and temporary/in-progress downloads
        if entry.is_dir():
            return

        name = entry.name
        ext = os.path.splitext(name)[1].lower()

        if ext in TEMP_EXTENSIONS:
            return

        # Find the matching destination folder
        for folder_name, extensions in dest_dirs.items():
            if ext not in extensions:
                continue

            # IMPORTANT:
            # Wait until Chrome/browser has finished writing the file.
            if not self.wait_until_stable(entry.path):
                return

            target_folder = os.path.join(source_dir, folder_name)
            target_path = os.path.join(target_folder, name)

            try:
                os.makedirs(target_folder, exist_ok=True)

                # Avoid overwriting an existing file
                if os.path.exists(target_path):
                    base, extension = os.path.splitext(name)
                    new_name = f"{base}_{int(time.time())}{extension}"
                    target_path = os.path.join(target_folder, new_name)

                shutil.move(entry.path, target_path)
                print(f"Moved: {name} -> {folder_name}/")

            except (PermissionError, FileNotFoundError, OSError) as e:
                print(f"Could not move {name}: {e}")

            break


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()

    print(f"Watching {source_dir} for changes...")
    print("Files are moved only after the download is complete.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
