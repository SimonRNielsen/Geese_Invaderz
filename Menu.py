import pygame
from AssetLoader import AssetLoader
from Enums import Assets
from Components import SpriteRenderer
from GameObject import GameObject
import time

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
    def __init__(self, game_world, menu):
        self._gameWorld = game_world
        self._screen = self._gameWorld.screen
        self._pos = pygame.math.Vector2(self._screen.get_width() / 2, self._screen.get_height() / 2)
        self._menu = menu




        self._gameObject = GameObject(self._pos)
        self._sr =self._gameObject.add_component(SpriteRenderer(Assets.BUTTON))


        self._image = AssetLoader.get_sprite(Assets.BUTTON)
        self.rect = self._image.get_rect(topleft=(self._pos))
        self._text = "Die geese"
        self._show_text =True
    

    def get_button(self):
        return self._gameObject
    
    def draw_text(self, text):
        self._font = pygame.font.SysFont("Inkfree", 60)
        self._text_surface = self._font.render(text, True, (0, 0, 0))
        self._text_rect = self._text_surface.get_rect()
        



    def klik_i_din_rumpe(self):
        if(self.rect.collidepoint(pygame.mouse.get_pos()) == True):
            if(self._sr.sprite_image == self._image):
                self._menu.destroy()
                self._gameObject.destroy()
                self._show_text = False
            #     self._sr.change_sprite(Assets.BUTTON_PRESSED)
            #     self._text = "Holy Morten"
            # else:
            #     self._sr.change_sprite(Assets.BUTTON)
    
    
    def update(self,delta_time):
        if (self._show_text == True):
            self.draw_text(self._text)
            self._text_rect.center = self.rect.center
            self._screen.blit(self._text_surface, self._text_rect)

    def awake(self, game_world):
        pass

    def start(self):
        pass

            