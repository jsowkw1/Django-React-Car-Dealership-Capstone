"""Opens a real console window running the Django dev server and captures it (Task 2). Windows only.

    python scripts/capture_terminal.py
The server keeps running in that window afterwards; close it when done.
"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from wincap import capture_window, find_window  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TITLE = 'Django Development Server'

subprocess.Popen(['cmd.exe', '/k', 'scripts\\run_django_server.bat'], cwd=ROOT,
                 creationflags=subprocess.CREATE_NEW_CONSOLE)

hwnd = None
for _ in range(30):
    time.sleep(1)
    hwnd = find_window(TITLE)
    if hwnd:
        break
if not hwnd:
    sys.exit('Console window not found')
time.sleep(8)  # let runserver finish its system checks and print the startup banner
out = ROOT / 'screenshots' / 'task02_django_server.png'
capture_window(hwnd, out, maximize=False)
print('saved', out)
