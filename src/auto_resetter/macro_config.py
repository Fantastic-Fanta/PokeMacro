from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple, Union

import pyautogui
import yaml

ClickDict = Dict[str, Any]
ClickTuple = Union[
    Tuple[int, int],
    Tuple[int, int, float],
    Tuple[int, int, float, int, int, int, int, int, float],
]
ClickConfig = Union[ClickDict, ClickTuple]


@dataclass(frozen=True)
class RegionConfig:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class PositionsConfig:
    egg_man_position: Tuple[int, int]
    event_button: Tuple[int, int]
    dialogue_yes: Tuple[int, int]
    menu_button: Tuple[int, int]
    quick_rejoin_sprite: Tuple[int, int]
    quick_rejoin_button: Tuple[int, int]
    save_button: Tuple[int, int]


def _load_config_from_yaml() -> Dict[str, Any]:
    config_path = Path(__file__).parent.parent.parent / "configs.yaml"
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        return {}


_config = _load_config_from_yaml()
_wishlist = _config.get("Wishlist", {})
RESKINS = _wishlist.get("Reskins", ["Whiteout", "Phantom", "Glitch"])
GRADIENTS = _wishlist.get("Gradients", ["Chronos", "Helios", "Gaia", "Nereus", "Nyx", "Frostbite", "Winter"])
USERNAME = _config.get("Username", "Manta")
DISCORD_WEBHOOK = _config.get("DiscordWebhook", "")
IS_RESKIN = _config.get("IsReskin", False)
IS_SHINY = _config.get("IsShiny", False)
IS_GRADIENT = _config.get("IsGradient", False)
IS_ANY = _config.get("IsAny", True)
IS_GOOD = _config.get("IsGood", False)


@dataclass
class MacroConfig:
    region: RegionConfig
    click_sequence: Sequence[ClickConfig]
    positions: PositionsConfig
    username: str = USERNAME
    reskins: Optional[Sequence[str]] = None
    gradients: Optional[Sequence[str]] = None
    is_reskin: bool = IS_RESKIN
    is_shiny: bool = IS_SHINY
    is_gradient: bool = IS_GRADIENT
    is_any: bool = IS_ANY
    is_good: bool = IS_GOOD
    initial_delay_seconds: float = 3.0
    post_click_delay_seconds: float = 1.0
    between_iterations_delay_seconds: float = 5.0
    discord_webhook: str = DISCORD_WEBHOOK
    
    def __post_init__(self) -> None:
        object.__setattr__(self, "reskins", self.reskins or RESKINS)
        object.__setattr__(self, "gradients", self.gradients or GRADIENTS)


def _to_tuple(value: Any) -> Tuple[int, int]:
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return (int(value[0]), int(value[1]))
    raise ValueError(value)


def _load_positions_from_yaml() -> PositionsConfig:
    positions_yaml = _config.get("Positions", {})
    get_pos = lambda key, default: _to_tuple(positions_yaml.get(key, default))
    return PositionsConfig(
        egg_man_position=get_pos("EggManPosition", [675, 739]),
        event_button=get_pos("EventButton", [1418, 965]),
        dialogue_yes=get_pos("DialogueYES", [1170, 405]),
        menu_button=get_pos("MenuButton", [43, 451]),
        quick_rejoin_sprite=get_pos("QuickRejoinSprite", [1475, 850]),
        quick_rejoin_button=get_pos("QuickRejoinButton", [1000, 580]),
        save_button=get_pos("SaveButton", [70, 735]),
    )


def _load_region_from_yaml() -> RegionConfig:
    chat_window_yaml = _config.get("ChatWindow", {})
    left_corner = _to_tuple(chat_window_yaml.get("LeftCorner", [13, 136]))
    right_corner = _to_tuple(chat_window_yaml.get("RightCorner", [440, 354]))
    return RegionConfig(
        x=left_corner[0],
        y=left_corner[1],
        width=right_corner[0] - left_corner[0],
        height=right_corner[1] - left_corner[1],
    )


def _get_screen_center() -> Tuple[int, int]:
    size = pyautogui.size()
    return (size.width // 2, size.height // 2)
_get_chat_window_center = lambda region: (region.x + region.width // 2, region.y + region.height // 2)


def _create_default_click_sequence(
    positions: PositionsConfig,
    screen_center: Tuple[int, int],
    chat_window_center: Tuple[int, int],
) -> Sequence[ClickConfig]:
    return [
        {
            "position": screen_center,
            "sleep": 1.5,
            "wait_for_pixel": {
                "position": (screen_center[0], screen_center[1] // 2),
                "color": (249, 239, 146),
                "timeout": 50.0,
            },
        },
        {
            "position": (screen_center[0], screen_center[1] // 6),
            "sleep": 0.2,
        },
        {
            "position": (screen_center[0], screen_center[1] // 6 + 20),
            "sleep": 0.1,
        },
        {
            "position": screen_center,
            "sleep": 1.5,
            "wait_for_pixel": {
                "position": screen_center,
                "color": (146, 252, 207),
                "timeout": 50.0,
            },
        },
        {
            "position": screen_center,
            "sleep": 0.1,
        },
        {
            "position": positions.egg_man_position,
            "sleep": 0.7,
            "wait_for_pixel": {
                "position": positions.menu_button,
                "color": (255, 255, 255),
                "timeout": 50.0,
            },
        },
        {
            "position": positions.egg_man_position,
            "sleep": 0.1,
            "button": "right",
        },
        {
            "position": positions.egg_man_position,
            "sleep": 0.2,
            "button": "right",
        },
        {
            "position": positions.dialogue_yes,
            "sleep": 0.2,
        },
        {
            "position": positions.dialogue_yes,
            "sleep": 0.2,
        },
        {
            "position": chat_window_center,
            "sleep": 0.2,
        },
    ]


DEFAULT_POSITIONS = _load_positions_from_yaml()
DEFAULT_REGION = _load_region_from_yaml()
SCREEN_CENTER = _get_screen_center()
CHAT_WINDOW_CENTER = _get_chat_window_center(DEFAULT_REGION)
DEFAULT_CLICK_SEQUENCE = _create_default_click_sequence(DEFAULT_POSITIONS, SCREEN_CENTER, CHAT_WINDOW_CENTER)

DEFAULT_MACRO_CONFIG = MacroConfig(
    region=DEFAULT_REGION,
    click_sequence=DEFAULT_CLICK_SEQUENCE,
    positions=DEFAULT_POSITIONS,
    username=USERNAME,
    reskins=RESKINS,
    gradients=GRADIENTS,
    is_reskin=IS_RESKIN,
    is_shiny=IS_SHINY,
    is_gradient=IS_GRADIENT,
    is_any=IS_ANY,
    is_good=IS_GOOD,
    discord_webhook=DISCORD_WEBHOOK,
)


