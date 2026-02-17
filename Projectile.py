import pygame
from Enums import Entities
from AssetLoader import AssetLoader
from Components import Component
#from Enums import Entities
#from AssetLoader import AssetLoader

class Projectile(Component):
    def __init__(self, speed=600, projectile_type="player", direction=1):
        """
        Docstring for __init__

        :param speed: Pixels pr second
        :param projectile_type: 'Player', 'Enemy', 'Boss'
        :param direction: 1 = right, -1 = left
        """

        super().__init__()
        self._speed = speed
        self._type = projectile_type 
        self._direction = direction
        self._transform = None
        self._screen = None
        self._sprite_image = None
    
    def awake(self, game_world):
        self._screen = game_world.screen
        self._game_world = game_world
        self._transform = self.gameObject.transform
        self._gameObject._damage = 1
        self._gameObject._is_destroyed = False
        # try:
        #     if self._type.lower() == "player":
        #         self._sprite_image = AssetLoader.get_sprite(Entities.PLAYER)  # eller lav en PLAYER_PROJECTILE
        #     elif self._type.lower() == "enemy":
        #         self._sprite_image = AssetLoader.get_sprite(Entities.ENEMY_PROJECTILE)
        #     elif self._type.lower() == "boss":
        #         self._sprite_image = AssetLoader.get_sprite(Entities.FIREBALL)
        # except Exception as e:
        #     self._sprite_image = None
        #     print(f"[projectile] Sprite for {self._type} ikke fundet: {e}")

    def start(self):
        pass

    def update(self, delta_time):
        #Flyt projectiles
        self._transform.position.x += self._speed * delta_time * self._direction

        #Tegn projectile hvis sprite findes
        # if self._sprite_image:
        #     self._screen.blit(self._sprite_image, self._transform.position)

        #Fjern hvis udenfor skærmen
        if self._transform.position.x < 0 or self._transform.position.x > self._screen.get_width():
            self._game_world._projectile_pool.return_object(self.gameObject)