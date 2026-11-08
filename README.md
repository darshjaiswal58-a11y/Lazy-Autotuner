# Downloads Cleaner 🧹

A lightweight Python-based automation tool that keeps your Downloads folder clean and organized. It monitors your Downloads directory in real time and automatically sorts downloaded files into dedicated folders based on their file types.

## ✨ Features

- **Real-Time Monitoring:** Automatically detects newly downloaded or modified files using the Watchdog library.
- **Automatic Organization:** Sorts files into categorized folders:
  - 📷 Images
  - 📄 Documents
  - 📦 Archives
  - 💿 Installers
  - 💻 Code Files
- **Download Completion Detection:** Waits until a file has finished downloading before moving it.
- **Temporary File Filtering:** Ignores incomplete downloads and temporary browser files.
- **Duplicate Protection:** Prevents existing files from being overwritten by generating unique filenames.
- **Lightweight:** Runs in the background with minimal resource usage.

## 🛠️ Technologies Used

- Python
- Watchdog
- OS
- Shutil
- Time

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install dependencies:
   ```bash
   pip install watchdog
   ```
3. Configure your Downloads folder path inside the Python script:
   ```python
   source_dir = r"E:\downloads"
   ```
4. Run the script:
   ```bash
   python cleaner.py
   ```

## 🎯 Purpose

Built to automate file management, reduce Downloads folder clutter, and demonstrate practical Python automation using filesystem event monitoring.

---

**Keep your Downloads folder clean, organized, and clutter-free!**