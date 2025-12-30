import sys
from typing import Optional

import pyautogui

if sys.platform == "win32":
    try:
        from pywinauto import Application
        from pywinauto.findwindows import ElementNotFoundError
        PYWINAUTO_AVAILABLE = True
    except ImportError:
        PYWINAUTO_AVAILABLE = False
else:
    PYWINAUTO_AVAILABLE = False


def is_windows() -> bool:
    return sys.platform == "win32"
def is_macos() -> bool:
    return sys.platform == "darwin"

class PlatformClicker:
    def __init__(self, roblox_window_title: str = "Roblox") -> None:
        self._is_windows = is_windows()
        self._roblox_window_title = roblox_window_title
        self._roblox_app: Optional[Application] = None
        
        if self._is_windows:
            self._find_roblox_window()
    
    def _find_roblox_window(self) -> None:
        if not self._is_windows:
            return
        methods = [
            lambda: Application(backend="uia").connect(title_re=self._roblox_window_title),
            lambda: Application(backend="uia").connect(class_name="RobloxApp"),
            lambda: Application(backend="uia").connect(process="RobloxPlayerBeta.exe"),
            lambda: Application(backend="win32").connect(title_re=self._roblox_window_title),
            lambda: Application(backend="win32").connect(class_name="RobloxApp"),
        ]
        
        for method in methods:
            try:
                self._roblox_app = method()
                return
            except (ElementNotFoundError, Exception):
                continue
        self._roblox_app = None
    
    def _ensure_roblox_connection(self) -> None:
        if not self._is_windows or self._roblox_app is not None:
            return
        
        try:
            self._find_roblox_window()
        except Exception as e:
            print(e)
    
    def click(self, x: int, y: int) -> None:
        if self._is_windows:
            self._click_windows(x, y, button="left")
        else:
            pyautogui.click(x, y)
    
    def right_click(self, x: int, y: int) -> None:
        if self._is_windows:
            self._click_windows(x, y, button="right")
        else:
            pyautogui.rightClick(x, y)
    
    def _click_windows(self, x: int, y: int, button: str = "left") -> None:
        self._ensure_roblox_connection()
        
        if self._roblox_app is None:
            if button == "right":
                pyautogui.rightClick(x, y)
            else:
                pyautogui.click(x, y)
            return
        
        try:
            main_window = self._roblox_app.top_window()
            rect = main_window.rectangle()
            window_x = rect.left
            window_y = rect.top
            rel_x = x - window_x
            rel_y = y - window_y
            if button == "right":
                main_window.click_input(button="right", coords=(rel_x, rel_y))
            else:
                main_window.click_input(coords=(rel_x, rel_y))
        except Exception as e:
            if button == "right":
                pyautogui.rightClick(x, y)
            else:
                pyautogui.click(x, y)

