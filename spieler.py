import arcade
import math

class Spieler(arcade.Sprite):

    def __init__(self, **kwargs):
        self.walking_textures = [
            arcade.load_texture("assets/PNG/Characters/walk1.png"),
            arcade.load_texture("assets/PNG/Characters/walk2.png"),     
        ]

        self.climb_textures = [
            arcade.load_texture("assets/PNG/Characters/climb1.png"),
            arcade.load_texture("assets/PNG/Characters/climb2.png"),
        ]

        self.klettert = False

        self.idle_texture = arcade.load_texture("assets/PNG/Characters/idle.png")
        self.jump_texture = arcade.load_texture("assets/PNG/Characters/jump.png")
        self.duck_texture = arcade.load_texture("assets/PNG/Characters/duck.png")

        super().__init__(self.idle_texture ,**kwargs)



        self.walk_texture_index = 0
        self.climb_texture_index = 0

        self.texture = self.textures[0]

        self.elapsed_time = 0
        self.walking_fps = 0.5
        self.kletter_fps = 0.5


    def update_animation(self, delta_time = 1 / 60, *args, **kwargs):
        self.elapsed_time += delta_time

        if self.klettert:
            self.texture = self.climb_textures[self.climb_texture_index]
            if self.elapsed_time > (1 / (self.kletter_fps * max(1, abs(self.change_y)))):
                self.elapsed_time = 0
                self.climb_texture_index = (self.climb_texture_index + 1) % (len(self.climb_textures))

        elif self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture

        elif self.change_y != 0 and not self.klettert:
                self.texture = self.jump_texture

        else:
            self.texture = self.walking_textures[self.walk_texture_index]
            if self.elapsed_time > (1 / (self.walking_fps * max(1, abs(self.change_x)))):
                self.elapsed_time = 0
                self.walk_texture_index = (self.walk_texture_index + 1) % len(self.walking_textures)
            
        self.scale_x = math.copysign(1, self.change_x)