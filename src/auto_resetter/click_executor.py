import time
from typing import Any, Dict, Optional, Sequence, Tuple

import pyautogui

from .macro_config import ClickConfig
from .pixel_utils import PixelColorService


class ClickExecutor:
    def __init__(self, pixel_service: Optional[PixelColorService] = None) -> None:
        self._pixel_service = pixel_service or PixelColorService()

    def _parse_click_config(
        self, click_config: ClickConfig
    ) -> Tuple[int, int, float, Optional[Dict[str, Any]], str]:
        if isinstance(click_config, dict):
            x, y = click_config["position"]
            sleep_time = float(click_config.get("sleep", 0))
            pixel_check = click_config.get("wait_for_pixel", None)
            button = click_config.get("button", "left").lower()
            return x, y, sleep_time, pixel_check, button
        
        if isinstance(click_config, tuple):
            if len(click_config) == 2:
                x, y = click_config
                return int(x), int(y), 0.0, None, "left"
            if len(click_config) == 3:
                x, y, sleep_time = click_config
                return int(x), int(y), float(sleep_time), None, "left"
            if len(click_config) == 9:
                (
                    x,
                    y,
                    sleep_time,
                    px_x,
                    px_y,
                    px_r,
                    px_g,
                    px_b,
                    px_timeout,
                ) = click_config
                pixel_check = {
                    "position": (int(px_x), int(px_y)),
                    "color": (int(px_r), int(px_g), int(px_b)),
                    "timeout": float(px_timeout),
                }
                return int(x), int(y), float(sleep_time), pixel_check, "left"

        raise ValueError(click_config)

    def execute_mouse_clicks(self, click_sequence: Sequence[ClickConfig]) -> None:
        for click_config in click_sequence:
            try:
                x, y, sleep_time, pixel_check, button = self._parse_click_config(
                    click_config
                )
            except ValueError as e:
                print(e)
                continue
            if pixel_check:
                pixel_pos = pixel_check["position"]
                pixel_color = pixel_check["color"]
                pixel_timeout = float(pixel_check.get("timeout", 10.0))
                if not self._pixel_service.wait_for_pixel_color(
                    pixel_pos[0], pixel_pos[1], pixel_color, pixel_timeout
                ):
                    print(pixel_pos, pixel_color)

            if button == "right":
                pyautogui.rightClick(x, y)
            else:
                pyautogui.click(x, y)
            
            if sleep_time > 0:
                time.sleep(sleep_time)


