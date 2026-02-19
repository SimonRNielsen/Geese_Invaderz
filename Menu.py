from typing import List
import pygame
from AssetLoader import AssetLoader
from Enums import Assets, Button_Types, GameEvents, SFX
from Components import SpriteRenderer
from GameObject import GameObject
import time

class Menu():
    def __init__(self, gameWorld, menu_type):
        self._menu_type = menu_type
        self._gameObject = GameObject(pygame.math.Vector2(0,0))
        self._gameWorld = gameWorld
        self._gameObject.add_component(SpriteRenderer(self._menu_type))
        self._gameObject.add_component(self)

        self._text_list = self._gameWorld.texts
        self._gameObject._name = menu_type


        if self._gameObject._name not in self._gameWorld._gameObjects:
            self._gameWorld.instantiate(self._gameObject)

            match self._menu_type:
                case Assets.START_MENU:             
                    self._start_button = Button(self._gameWorld, self, Button_Types.START)
                    self._gameWorld.instantiate(self._start_button.get_button())
                    self._exit_button = Button(self._gameWorld, self, Button_Types.EXIT)
                    self._gameWorld.instantiate(self._exit_button.get_button())
                case Assets.PAUSE:
                    self._exit_button = Button(self._gameWorld, self, Button_Types.EXIT)
                    self._gameWorld.instantiate(self._exit_button.get_button())
                    self._resume_button = Button(self._gameWorld, self, Button_Types.RESUME)
                    self._gameWorld.instantiate(self._resume_button.get_button())
                    self._main_button = Button(self._gameWorld, self, Button_Types.MAIN)
                    self._gameWorld.instantiate(self._main_button.get_button())
                case Assets.WIN_SCREEN:
                    self._restart_button = Button(self._gameWorld, self, Button_Types.RESTART)
                    self._gameWorld.instantiate(self._restart_button.get_button())
                    self._exit_button = Button(self._gameWorld, self, Button_Types.EXIT)
                    self._gameWorld.instantiate(self._exit_button.get_button())
                    self._main_button = Button(self._gameWorld, self, Button_Types.MAIN)
                    self._gameWorld.instantiate(self._main_button.get_button())
                    self._killed_button = Button(self._gameWorld, self, Button_Types.KILLED)
                    self._gameWorld.instantiate(self._killed_button.get_button())
                case Assets.LOOSE_SCREEN:
                    self._restart_button = Button(self._gameWorld, self, Button_Types.RESTART)
                    self._gameWorld.instantiate(self._restart_button.get_button())
                    self._exit_button = Button(self._gameWorld, self, Button_Types.EXIT)
                    self._gameWorld.instantiate(self._exit_button.get_button())
                    self._main_button = Button(self._gameWorld, self, Button_Types.MAIN)
                    self._gameWorld.instantiate(self._main_button.get_button())
                    self._killed_button = Button(self._gameWorld, self, Button_Types.KILLED)
                    self._gameWorld.instantiate(self._killed_button.get_button())


    @property
    def menu_type(self):
        return self._menu_type
    

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
        self._main_menu_bool = False

        

        #Position of the button
        match self._button_type:
            case Button_Types.START:
                self._pos = pygame.math.Vector2(800, 600)
            case Button_Types.EXIT:
                self._pos = pygame.math.Vector2(1000,600)
            case Button_Types.RESTART:
                self._pos = pygame.math.Vector2(800, 600)
            case Button_Types.RESUME:
                self._pos = pygame.math.Vector2(800, 600)
            case Button_Types.MAIN:
                self._pos = pygame.math.Vector2(900, 700)
            case Button_Types.KILLED:
                # self._pos = pygame.math.Vector2(self._screen.get_width()/2, 400)
                self._pos = pygame.math.Vector2(1000,500)
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

        #Text on the button
        if(self._button_type == Button_Types.KILLED):
            self._text = str(self._gameWorld.killed_enemies)
        else:
            self._text = button_type.name
        self._gameWorld.add_to_text_button(self)


        #Text
        self._font = pygame.font.SysFont("CopperplateGothicBold", 30)
        self._text_surface = self._font.render(self._text, True, (0, 0, 0))
        self._text_rect = self._text_surface.get_rect(center=self.rect.center)

        self._main_amount = 0
        self._gameWorld.texts.append(self)
                
    

    def get_button(self):
        return self._gameObject
    
    # def draw_text(self, text):
    #     self._font = pygame.font.SysFont("CopperplateGothicBold", 30)
    #     self._text_surface = self._font.render(text, True, (0, 0, 0))
    #     self._text_rect = self._text_surface.get_rect()
        

    def click_on_button(self):
        if(self.rect.collidepoint(pygame.mouse.get_pos()) == True):
            self._gameWorld._sound_manager.play_sound(SFX.BUTTON_CLICK)
            match self._button_type:
                case Button_Types.EXIT:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                case Button_Types.MAIN:
                    self._gameWorld.player_alive.is_destroyed = False
                    self._main_amount += 1
                case Button_Types.RESTART:
                    self._gameWorld.player_alive.is_destroyed = False
                    self._gameWorld.reset_game_bool = True
                case Button_Types.START:
                    self._gameWorld.player_alive.is_destroyed = False
                    self._gameWorld.reset_game_bool = True

            self._menu.get_menu().destroy()
            self._gameWorld.menu_bool = False
            self._gameWorld.pause_bool = False

            for text_and_button in self._texts:
                text_and_button._show_text = False
                text_and_button.get_button().destroy()

            if(self._main_amount == 1):
                self._main_menu_bool = True
                self._gameWorld.menu_bool = True          
    
    
    def update(self,delta_time):
        if (self._show_text == True):
            # self.draw_text(self._text)
            self._text_rect.center = self.rect.center
            self._screen.blit(self._text_surface, self._text_rect)
        if self._main_menu_bool == True:
            Menu(self._gameWorld, Assets.START_MENU)
            self._main_menu_bool = False


    def awake(self, game_world):
        pass

    def start(self):
        pass

            