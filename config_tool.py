from src.auto_resetter.pixel_utils import PixelColorService
import time

# Use this for quick configurations

if __name__ == "__main__":
    pixel_service = PixelColorService()
    time.sleep(3)

    x, y, r, g, b = pixel_service.get_pixel_color_at_mouse()
    print(f"Position: ({x}, {y})")
    print(f"RGB: ({r}, {g}, {b})")

