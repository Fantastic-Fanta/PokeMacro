import pyautogui

from .macro_config import DEFAULT_MACRO_CONFIG
from .macro_runner import MacroRunner


def main() -> None:
    pyautogui.FAILSAFE = True
    runner = MacroRunner(DEFAULT_MACRO_CONFIG)
    runner.run()


if __name__ == "__main__":
    main()


