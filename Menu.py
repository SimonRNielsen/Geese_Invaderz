from typing import List
import pygame
from AssetLoader import AssetLoader
from Enums import Assets, Button_Types
from Components import SpriteRenderer
from GameObject import GameObject
import time

class Menu():
    def __init__(self, gameWorld, menu_type):
        self._menu_type = menu_type
        self._gameObject = GameObject(pygame.math.Vector2(0,0))
        self._gameWorld = gameWorld
        # self._screen = self._gameWorld.screen
        self._gameObject.add_component(SpriteRenderer(self._menu_type))






        match self._menu_type:
            case Assets.START_MENU:
                
                self._start_button = Button(self._gameWorld, self, Button_Types.START)
                self._gameWorld.instantiate(self._start_button.get_button())
                self._gameWorld.add_to_text_button(self._start_button)
                self._exit_button = Button(self._gameWorld, self, Button_Types.EXIT)
                self._gameWorld.instantiate(self._exit_button.get_button())
                self._gameWorld.add_to_text_button(self._exit_button)



    @property
    def menu_type(self):
        return self._menu_type


    def show_pause(self):
        self._gameObject.add_component(SpriteRenderer(self._menu_type))
    

    def get_menu(self):
        return self._gameObject
    
    def update(self,delta_time):
        pass


    def awake(self, game_world):
        pass

    def start(self):
        pass


class Button():
    def __init__(self, game_world, menu, button_type):
        self._gameWorld = game_world
        self._screen = self._gameWorld.screen
        self._menu = menu
        self._button_type = button_type
        self._texts: List[Button] = self._gameWorld.texts        
        

        #Position of the button
        match self._button_type:
            case Button_Types.START:
                self._pos = pygame.math.Vector2(800, 550)
            case Button_Types.EXIT:
                self._pos = pygame.math.Vector2(1000,550)
            case Button_Types.RESTART:
                self._pos = pygame.math.Vector2(self._screen.get_width() / 2, self._screen.get_height() / 2)
            case Button_Types.RESUME:
                self._pos = pygame.math.Vector2(self._screen.get_width() / 2, self._screen.get_height() / 2)
            case Button_Types.MAIN_MENU:
                self._pos = pygame.math.Vector2(self._screen.get_width() / 2, self._screen.get_height() / 2 + 100)
            case _:
                print(f"No match case for {button_type} in Button.__init__")
                self._pos = pygame.math.Vector2(self._screen.get_width() / 2, self._screen.get_height() / 2)

        #GameObject and SpriteRenderer for the button
        self._gameObject = GameObject(self._pos)
        self._sr =self._gameObject.add_component(SpriteRenderer(Assets.BUTTON))

        #Text on the button
        self._image = AssetLoader.get_sprite(Assets.BUTTON)
        self.rect = self._image.get_rect(topleft=(self._pos))
        self._show_text =True
        pygame.sprite.LayeredUpdates.move_to_front(self)

        #Text on the button
        self._text = button_type.name
                

    

    def get_button(self):
        return self._gameObject
    
    def draw_text(self, text):
        self._font = pygame.font.SysFont("timesnerroman", 30)
        self._text_surface = self._font.render(text, True, (0, 0, 0))
        self._text_rect = self._text_surface.get_rect()
        



    def klik_i_din_rumpe(self):
        if(self.rect.collidepoint(pygame.mouse.get_pos()) == True):
            if(self._button_type == Button_Types.START):
                self._menu.get_menu().destroy()
            elif(self._button_type == Button_Types.EXIT):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            for text_and_button in self._texts:
                text_and_button._show_text = False
                text_and_button.get_button().destroy()
    
    
    def update(self,delta_time):
        if (self._show_text == True):
            self.draw_text(self._text)
            self._text_rect.center = self.rect.center
            self._screen.blit(self._text_surface, self._text_rect)

    def awake(self, game_world):
        pass

    def start(self):
        pass

            