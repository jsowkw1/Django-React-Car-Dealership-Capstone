"""Windows helper: capture a real top-level window (including browser chrome and address bar).

Finds a visible window by a title substring, brings it to the foreground and grabs
its on-screen pixels with mss. Windows only.
"""
import ctypes
import time
from ctypes import wintypes

import mss
import mss.tools

user32 = ctypes.windll.user32
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # per-monitor DPI aware -> physical pixels
except Exception:  # noqa: BLE001
    user32.SetProcessDPIAware()

EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def _title(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def _pid(hwnd):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def find_window(substring='', pids=None):
    """First visible window whose title contains `substring` (and, if given, owned by one of `pids`)."""
    found = []

    def callback(hwnd, _):
        if user32.IsWindowVisible(hwnd) and (pids is None or _pid(hwnd) in pids):
            title = _title(hwnd)
            if title and substring in title:
                found.append(hwnd)
        return True

    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return found[0] if found else None


def browser_pids(profile_marker):
    """PIDs of browser processes started with a user-data-dir containing `profile_marker`."""
    import psutil

    pids = set()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        cmd = ' '.join(proc.info['cmdline'] or [])
        if profile_marker in cmd and '--type=' not in cmd:
            pids.add(proc.info['pid'])
    return pids


def window_rect(hwnd):
    rect = wintypes.RECT()
    # DWMWA_EXTENDED_FRAME_BOUNDS excludes the invisible resize borders
    if ctypes.windll.dwmapi.DwmGetWindowAttribute(hwnd, 9, ctypes.byref(rect), ctypes.sizeof(rect)) != 0:
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom


def bring_to_front(hwnd, maximize=True):
    user32.ShowWindow(hwnd, 3 if maximize else 9)  # SW_MAXIMIZE / SW_RESTORE
    # Pressing/releasing ALT lets this process take the foreground.
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    time.sleep(0.6)


def click_at(x, y):
    user32.SetCursorPos(int(x), int(y))
    user32.mouse_event(0x0002, 0, 0, 0, 0)  # left down
    user32.mouse_event(0x0004, 0, 0, 0, 0)  # left up
    time.sleep(0.4)


def capture_window(hwnd, path, maximize=True, focus_page=False):
    bring_to_front(hwnd, maximize)
    left, top, right, bottom = window_rect(hwnd)
    if focus_page:
        # A real click on the empty bottom-left page margin moves keyboard focus out of
        # the address bar (so the URL is not shown highlighted), then park the cursor.
        click_at(left + 6, bottom - 6)
        user32.SetCursorPos(right - 40, bottom - 40)
        time.sleep(0.3)
    with mss.mss() as sct:
        shot = sct.grab({'left': left, 'top': top, 'width': right - left, 'height': bottom - top})
        mss.tools.to_png(shot.rgb, shot.size, output=str(path))
    return path
