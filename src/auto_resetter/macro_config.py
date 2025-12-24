from dataclasses import dataclass
from typing import Any, Dict, Sequence, Tuple, Union


ClickDict = Dict[str, Any]
ClickTuple = Union[
    Tuple[int, int],
    Tuple[int, int, float],
    Tuple[int, int, float, int, int, int, int, int, float],
]
ClickConfig = Union[ClickDict, ClickTuple]


@dataclass
class RegionConfig:
    x: int
    y: int
    width: int
    height: int


# CONFIGS - Change if necessary (Most likely very necessary please do actually change it based on screen res)


@dataclass
class MacroConfig:
    region: RegionConfig
    click_sequence: Sequence[ClickConfig]
    keywords: Sequence[str]
    initial_delay_seconds: float = 3.0
    post_click_delay_seconds: float = 1.0
    between_iterations_delay_seconds: float = 5.0


DEFAULT_REGION = RegionConfig(  # Chat window dimensions
    x=10,
    y=130,
    width=460,
    height=220,
)

DEFAULT_CLICK_SEQUENCE: Sequence[ClickConfig] = [  # Default egg sequence example
    {
        "position": (745, 920),  # Await main loading screen
        "sleep": 1.5,
        "wait_for_pixel": {
            "position": (
                387,
                311,
            ),  # Pos of some random place on the Pokemon big word thing (that's yellow)
            "color": (249, 239, 146),  # Pokemon text filler - Yellow
            "timeout": 50.0,
        },
    },
    (745, 920, 1),
    (745, 900, 0.1),  # Double click at random point of screen incase of no reg
    {
        "position": (1000, 400),  # Pos of the green save loading card
        "sleep": 1.5,
        "wait_for_pixel": {
            "position": (1000, 400),
            "color": (146, 252, 207),  # Normal mode save slot UI - Green
            "timeout": 50.0,
        },
    },
    (1000, 400, 0.1),  # Assurance click once again
    {
        "position": (762, 523),  # [MUST CHANGE] Egg man npc position
        "sleep": 0.2,
        "wait_for_pixel": {
            "position": (
                1418,
                965,
            ),  # Position of the "Events" button UI at bottom right corner
            "color": (199, 115, 247),  # Event button - pink
            "timeout": 50.0,
        },
    },
    (1170, 405, 0.1),  # Position of the dialogue [YES]
    (1170, 405, 0.1),
    (1170, 405, 0.1),
    
    (1170, 405, 0.1),
    (1170, 405, 0.1),
    (1170, 405, 0.1),
    
    (1170, 405, 0.1),
    (1170, 405, 0.1),
    (1170, 405, 0.1),
    
    (1170, 405, 0.1),
    (1170, 405, 0.1),
    (1170, 405, 0.1),

    (1170, 405, 0.1),
    
    (200, 300, 0.1),  # Chat window to focus in
]


# DEFAULT_KEYWORDS = ("Your username", "Gradient/Reskin Name/Shiny")
# Example: this will look for when `Manta`, `Shiny` and `Nereus` all appear in the same body of text.
DEFAULT_KEYWORDS = ("Manta", "Shiny", "Nereus")


DEFAULT_MACRO_CONFIG = MacroConfig(
    region=DEFAULT_REGION,
    click_sequence=DEFAULT_CLICK_SEQUENCE,
    keywords=DEFAULT_KEYWORDS,
)


