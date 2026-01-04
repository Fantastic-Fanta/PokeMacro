import time
from pathlib import Path
from typing import Optional

import pyautogui

from .click_executor import ClickExecutor
from .discord_webhook import send_discord_webhook
from .img_funcs import (
    OcrService,
    ScreenRegion,
    matches_config,
    trim_text_from_username_to_attempts,
    remove_chronos_event_phrase,
)
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
        self._log_file_path = Path(__file__).parent.parent.parent / "history.log"

    def _matches_config(self, text: str) -> bool:
        return matches_config(
            text,
            self._config.username,
            self._config.reskins,
            self._config.gradients,
            self._config.is_reskin,
            self._config.is_shiny,
            self._config.is_gradient,
            self._config.is_any,
            self._config.is_good,
        )

    def run(self) -> None:
        time.sleep(self._config.initial_delay_seconds)
        
        while True:
            self._click_executor.execute_mouse_clicks(self._config.click_sequence)
            time.sleep(self._config.post_click_delay_seconds)
            
            image = self._screen_region.capture()
            text = trim_text_from_username_to_attempts(
                remove_chronos_event_phrase(self._ocr_service.extract_text(image)),
                self._config.username
            )
            
            if self._config.username.lower() in text.lower():
                self._log_username_detection(text)
            
            if self._matches_config(text):
                self._handle_match_found()
                break
            
            self._handle_no_match()
            time.sleep(self._config.between_iterations_delay_seconds)

    def _handle_match_found(self) -> None:
        positions = self._config.positions
        
        if self._config.discord_webhook:
            send_discord_webhook(
                self._config.discord_webhook,
                "@everyone **Found something tuff boiiiii!!!",
                username="W AURA W LUCK W MANTA W SHROODLE CAN WE GET A W IN DA CHAT FOR DIS W LIL RAT YO!"
            )
        
        for _ in range(3):
            pyautogui.click(*positions.dialogue_yes)
            time.sleep(0.2)
        
        pyautogui.click(*positions.menu_button)
        time.sleep(2)
        pyautogui.click(*positions.save_button)
        time.sleep(2)
        pyautogui.click(*positions.dialogue_yes)

    def _handle_no_match(self) -> None:
        positions = self._config.positions
        pyautogui.click(*positions.quick_rejoin_sprite)
        time.sleep(0.2)
        pyautogui.click(*positions.quick_rejoin_button)

    def _log_username_detection(self, text: str) -> None:
        with open(self._log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{text}\n{'=' * 80}\n")
        
        if self._config.discord_webhook:
            send_discord_webhook(
                self._config.discord_webhook,
                f"```\n{text}\n```",
                username="Poopimon Notifier"
            )
