import pygame
from AssetLoader import AssetLoader
from Enums import Assets
from Components import SpriteRenderer
from GameObject import GameObject
import mouse

class Menu():
    def __init__(self):
        self._gameObject = GameObject(pygame.math.Vector2(0,0))
        self._gameObject.add_component(SpriteRenderer(Assets.START_MENU))
    

    def get_menu(self):
        return self._gameObject
    
    def update(self,delta_time):
        pass

    def awake(self, game_world):
        pass

    def start(self):
        pass

class Button():
    def __init__(self, game_world):
        self._gameWorld = game_world
        self._screen_size = self._gameWorld.screen
        self._pos = pygame.math.Vector2(self._screen_size.get_width() / 2, self._screen_size.get_height() / 2)





        self._gameObject = GameObject(self._pos)
        self._sr =self._gameObject.add_component(SpriteRenderer(Assets.BUTTON))


        self._image = AssetLoader.get_sprite(Assets.BUTTON)
        # self._image_size = self._image.get_size()
        self.rect = self._image.get_rect(topleft=(self._pos))
    

    def get_button(self):
        return self._gameObject
    
    def update(self,delta_time):
        pass

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def klik_i_din_rumpe(self):
        if(self.rect.collidepoint(pygame.mouse.get_pos()) == True):
            self._gameObject.destroy()
            print(self._gameObject.is_destroyed)