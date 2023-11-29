from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader, unlit_shader
from perlin_noise import PerlinNoise

import random
import pickle

from ui import Menu
app = Ursina()

block_textures = [
    load_texture('assets/grass.png'), #0
    load_texture('assets/gold.png'), #1 
    load_texture('assets/lava.png'), #2
    load_texture('assets/stone.png'), #3
]

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model = "sphere",
            texture = load_texture("assets/sky.jpg"),
            scale = 500,
            double_sided =  True,
            shader = unlit_shader,
            eternal = True,
        )


class Arm(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model = "assets/arm",
            texture = load_texture("assets/arm_texture.png"),
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6),
            eternal = True,
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)    

class Block(Button):
    id = 0
    def __init__(self, position = (0,0,0), id = 0):
        super().__init__(
            parent=scene,
            model = "assets/block",
            texture = block_textures[id],
            scale = 0.5,
            position = position,
            origin_y = 0.5,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            highlight_color=color.gray,
            shader = basic_lighting_shader,
        )
        self.id = id

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                arm.active()
                block = Block(position = self.position + mouse.normal, id=Block.id)
                game.blocks.append(block)
            elif key == "right mouse down":
                arm.active()
                destroy(self)
                game.blocks.remove(self)
            else:
                arm.passive()


class GameController(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        player.jumping = True
        player.jump_height = 3
        player.jump_up_duration = .3
        player.start_pos = player.position
        self.blocks = []
        self.menu = Menu(actions = [self.load, self.save, self.new_game, application.quit])
        arm.disable()
        application.paused = True



    def update(self):
        for i in range(1, len(block_textures)+1):
            if held_keys[str(i)]:
                Block.id = i-1
        if player.y < -50:
            player.position = player.start_pos

        if held_keys['shift']:
            player.speed = 10
        else:
            player.speed = 5
    
    def input(self, key):
        if key == 'k':
            self.save()
        if key == 'n':
            self.new_game()
        if key == 'l':
            self.load()

    def new_game(self):
        for block in self.blocks:
            destroy(block)
        
        self.blocks.clear()
        noise = PerlinNoise(octaves = 5,seed=random.randint(1,1000))
        
        for z in range(40):
            for x in range(40):
                height = noise([x*0.02, z*0.02])
                height = math.floor(height*7.5)
                block = Block(position=(x, height, z))
                self.blocks.append(block)

        player.position =(0, 25, 0)


    def save(self):
        with open("save.dat", "wb") as file:
            k = len(self.blocks)
            pickle.dump(k, file)
            for block in self.blocks:
                pickle.dump(block.position, file)
                pickle.dump(block.id, file)

            pickle.dump(player.position, file)

    def load (self):
        for block in self.blocks:
            destroy(block)
            self.blocks.clear()
        
        with open("save.dat", "rb")as file:
            k = pickle.load(file)
            for i in range(k):
                pos = pickle.load(file)
                id = pickle.load(file)
                block = Block(position = pos, id= id)
                self.blocks.append(block)
            
            player.position = pickle.load(file)
            player.start_pos = player.position






sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
sky = Sky()
player = FirstPersonController()
arm = Arm()

game = GameController()


app.run()

