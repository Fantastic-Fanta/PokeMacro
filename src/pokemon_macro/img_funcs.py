from dataclasses import dataclass

import pyautogui
import pytesseract
from PIL import Image


@dataclass
class ScreenRegion:
    x: int
    y: int
    width: int
    height: int

    def capture(self) -> Image.Image:
        screenshot = pyautogui.screenshot(
            region=(self.x, self.y, self.width, self.height)
        )
        screenshot.save("screenshot.png")
        return screenshot


class OcrService:
    def extract_text(self, image: Image.Image) -> str:
        try:
            return pytesseract.image_to_string(image)
        except Exception as exc:
            print(f"Error during OCR: {exc}")
            return "PMO"


contains_all_keywords = lambda text, keywords: all(
    keyword.lower() in text.lower() for keyword in keywords
)


