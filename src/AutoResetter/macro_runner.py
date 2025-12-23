import time
from typing import Optional

import pyautogui

from .click_executor import ClickExecutor
from .img_funcs import OcrService, ScreenRegion, contains_all_keywords
from .macro_config import DEFAULT_MACRO_CONFIG, MacroConfig


class MacroRunner:
    def __init__(
        self,
        config: MacroConfig,
        click_executor: Optional[ClickExecutor] = None,
        ocr_service: Optional[OcrService] = None,
    ) -> None:
        self._config = config
        self._click_executor = click_executor or ClickExecutor()
        self._ocr_service = ocr_service or OcrService()
        self._screen_region = ScreenRegion(
            x=config.region.x,
            y=config.region.y,
            width=config.region.width,
            height=config.region.height,
        )

    def run(self) -> None:
        time.sleep(self._config.initial_delay_seconds)
        matched = lambda text: contains_all_keywords(
            text, tuple(self._config.keywords)
        )
        iteration = 0
        while True:
            iteration += 1
            self._click_executor.execute_mouse_clicks(self._config.click_sequence)
            time.sleep(self._config.post_click_delay_seconds)
            image = self._screen_region.capture()
            text = self._ocr_service.extract_text(image)
            if matched(text):
                self._handle_match_found(text)
                break
            self._handle_no_match()
            time.sleep(self._config.between_iterations_delay_seconds)

    def _handle_match_found(self, text: str) -> None:
        pyautogui.click(21, 485)
        time.sleep(2)
        pyautogui.click(70, 732)
        time.sleep(2)
        pyautogui.click(1172, 366)

    def _handle_no_match(self) -> None:
        pyautogui.click(1470, 860)
        time.sleep(0.2)
        pyautogui.click(900, 580)


def main() -> None:
    """
    Entrypoint for running the macro with the default configuration.
    macOS: ensure Accessibility permissions are granted for automation.
    """
    runner = MacroRunner(DEFAULT_MACRO_CONFIG)
    runner.run()


if __name__ == "__main__":
    main()


