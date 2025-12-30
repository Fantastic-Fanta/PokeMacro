import time
from dataclasses import dataclass
from typing import Tuple

import mss
import numpy as np
import pyautogui


@dataclass
class PixelColorService:
    tolerance: int = 5 # Edit this if necessary; this is incase of your UI colors being imperfect or effected by lighting
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            b, g, r = img[0, 0, 0], img[0, 0, 1], img[0, 0, 2]
            return int(r), int(g), int(b)

    def get_pixel_color_at_mouse(self) -> Tuple[int, int, int, int, int]:
        x, y = pyautogui.position()
        r, g, b = self.get_pixel_color(x, y)
        return x, y, r, g, b

    def wait_for_pixel_color(
        self,
        x: int,
        y: int,
        target_color: Tuple[int, int, int],
        timeout: float = 10.0,
        check_interval: float = 0.1,
    ) -> bool:
        start_time = time.time()
        target_r, target_g, target_b = target_color

        def within_tolerance(current: int, target: int) -> bool:
            return abs(current - target) <= self.tolerance

        while time.time() - start_time < timeout:
            current_r, current_g, current_b = self.get_pixel_color(x, y)
            if (
                within_tolerance(current_r, target_r)
                and within_tolerance(current_g, target_g)
                and within_tolerance(current_b, target_b)
            ):
                return True

            time.sleep(check_interval)

        return False


