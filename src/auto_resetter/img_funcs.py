import re
from dataclasses import dataclass
from typing import Sequence

import pyautogui
import pytesseract
from PIL import Image


@dataclass(frozen=True)
class ScreenRegion:
    x: int
    y: int
    width: int
    height: int

    def capture(self, save_debug: bool = False) -> Image.Image:
        screenshot = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
        if save_debug:
            screenshot.save("screenshot.png")
        return screenshot


class OcrService:
    def extract_text(self, image: Image.Image) -> str:
        try:
            return pytesseract.image_to_string(image).strip()
        except Exception as exc:
            print(f"OCR screwed up: {exc}")
            return "Utterly Pmoed"


remove_chronos_event_phrase = lambda text: re.sub(r'\s+', ' ', re.sub(r'\b[Cc]hronos\s+[Ee]vent\s+2025\s+is\s+out\b', '', text, flags=re.IGNORECASE)).strip()


def trim_text_from_username_to_attempts(text: str, username: str) -> str:
    text_lower, username_lower = text.lower(), username.lower()
    
    if username_lower not in text_lower:
        return text
    
    username_index = text_lower.find(username_lower)
    if username_index == -1:
        return text

    search_text_lower = text_lower[username_index:]
    attempts_index = search_text_lower.find("attempts")
    
    if attempts_index == -1:
        return text[username_index:]
    
    return text[username_index:username_index + attempts_index + len("attempts")]


def matches_config(
    text: str,
    username: str,
    reskins: Sequence[str],
    gradients: Sequence[str],
    is_reskin: bool,
    is_shiny: bool,
    is_gradient: bool,
    is_any: bool,
    is_good: bool,
) -> bool:
    text_lower, username_lower = text.lower(), username.lower()
    
    if "attemp" not in text_lower or username_lower not in text_lower:
        return False
    
    has_reskin = any(reskin.lower() in text_lower for reskin in reskins)
    has_gradient = any(gradient.lower() in text_lower for gradient in gradients)
    has_shiny = "shiny" in text_lower
    
    checks = [
        lambda: not is_any or (has_reskin or has_gradient),
        lambda: not is_reskin or has_reskin,
        lambda: not is_shiny or has_shiny,
        lambda: not is_gradient or has_gradient,
        lambda: not is_good or ((has_reskin and has_gradient) or (has_shiny and has_gradient)),
    ]
    
    return all(check() for check in checks)