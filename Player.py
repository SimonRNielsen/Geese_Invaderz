import pygame
from AssetLoader import AssetLoader
from Enums import Entities
from Components import Component, SpriteRenderer
from GameObject import GameObject
from Projectile import Projectile

class Player(Component):
    def __init__(self, speed=400):
        super().__init__()
        self._speed = speed
        self._screen_height = None
        self._shoot_cooldown = 0.50
        self._time_since_last_shot = 0

    def awake(self, gameWorld):
        #Gem reference til skærmen, så der kan laves højdegrænser
        self._screen_height = gameWorld.screen.get_height()
        self._game_world = gameWorld

    def start(self):
        pass
            
    def update(self, delta_time):
        if self.gameObject is None:
            return
        
        keys = pygame.key.get_pressed()

        direction = 0
        if keys[pygame.K_w]:
            direction -= 1
        if keys[pygame.K_s]:
            direction += 1
                
        #Vertical movement
        transform = self.gameObject.transform
        transform.position.y += direction * self._speed * delta_time

        #Clamp så player ikke kan bevæge sig udenfor skærmens grænser
        sprite_height = self.gameObject.get_component("SpriteRenderer").sprite_image.get_height()
        if transform.position.y < 0:
            transform.position.y = 0
        elif transform.position.y > self._screen_height - sprite_height:
            transform.position.y = self._screen_height - sprite_height
        
        #Shoot
        self._time_since_last_shot += delta_time
        if keys[pygame.K_SPACE] and self._time_since_last_shot >= self._shoot_cooldown:
            self.shoot()
            self._time_since_last_shot = 0

    def shoot(self):
        #Spawn projectile infront of player
        sr = self.gameObject.get_component("SpriteRenderer")
        
        #Fallback hvis ingen sprite
        if sr.sprite_image:
            sprite_width = sr.sprite_image.get_width()
            sprite_height = sr.sprite_image.get_height()
        else:
            sprite_width = 50
            sprite_height = 50
        
        pos = self.gameObject.transform.position + pygame.math.Vector2(
            sprite_width,
            sprite_height // 2
        )
        proj_obj = GameObject(pos)
        proj_obj.add_component(SpriteRenderer(Entities.FIREBALL))
        proj_obj.add_component(Projectile(
            speed = 700,
            projectile_type = "boss", #Can be 'Player', 'Enemy', 'Boss'
            direction = 1 #Player shoots to the right
        ))
        self._game_world.instantiate(proj_obj)