import pygame
from AssetLoader import AssetLoader
from Enums import Assets
from Components import SpriteRenderer
from GameObject import GameObject

class Menu:
    def __init__(self):
        self._gameObject = GameObject(pygame.math.Vector2(0,0))
        self._gameObject.add_component(SpriteRenderer(Assets.START_MENU))
    

    def show_menu(self):
        return self._gameObject