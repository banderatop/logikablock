from ursina import * 


class Menu (Entity):
    def __init__(self, actions, add_to_scene_entities=True, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused = True, **kwargs)

        self.main_menu = Entity(parent = self, enable=True)
        self.bg = Sprite (parent = self.main_menu,scale = 0.22, texture="assets/sky.jpg", color = color.dark_gray, z=1)