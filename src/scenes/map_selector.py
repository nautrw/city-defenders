from src.maps.data import MAPS_DATA
from typing import TYPE_CHECKING
import pygame
from enum import Enum, auto
import src.core.config as Config
from src.core.scenes_manager import Scene
from src.gui.button import Button
from src.gui.gui_manager import GUIManager
from src.gui.placement_system import RectAnchorMode


if TYPE_CHECKING:
    from src.app import GameApp

class MapSelectorSceneGUIState(Enum):
    NORMAL = auto()
    
class MapSelectorSceneGUIManager(GUIManager):
    def __init__(self, scene: "MapSelectorScene") -> None:
        default_state = MapSelectorSceneGUIState.NORMAL
        
        super().__init__(scene, default_state)
        self.refresh()
    
    def refresh(self):
        if self.state == MapSelectorSceneGUIState.NORMAL:
            pass
    
    def handle_event(self, event: pygame.Event) -> None:
        pass

class MapSelectorScene(Scene):
    def __init__(self, game: "GameApp"):
        super().__init__(game)
        
        self.gui_manager = MapSelectorSceneGUIManager(self)

        self.all_maps = MAPS_DATA.keys()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(Config.DARK_BG)

        self.gui_manager.render_elements(surface)
    
    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            self.gui_manager.handle_event(event)
    
    def update(self, delta_time: float) -> None:
        pass