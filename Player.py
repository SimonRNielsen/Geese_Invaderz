import pygame
from AssetLoader import AssetLoader
from Enums import Entities, GameEvents, Components, Collisions, SFX
from Components import Component, SpriteRenderer, Collider
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
        self._gameObject._entity_type = Entities.PLAYER
        self._gameObject._health = 3
        sr = self.gameObject.get_component("SpriteRenderer")
        self._sprite_height = sr.sprite_image.get_height()
        self._sprite_width = sr.sprite_image.get_width()
        gameWorld.subscribe(GameEvents.ENEMY_ESCAPED, self.enemy_escaped)

    def start(self):
        collider = self.gameObject.get_component(Components.COLLIDER.value)
        collider.subscribe(Collisions.PIXEL_ENTER, self.take_damage)
        self._entity = self.gameObject.get_component("Entity")
            
    def update(self, delta_time):
        if self.gameObject is None:
            return
        
        keys = pygame.key.get_pressed()

        direction = 0
        if keys[pygame.K_w]:
            direction -= 1
        if keys[pygame.K_s]:
            direction += 1
        
        self._game_world._sound_manager.play_footsteps(direction)

        #Vertical movement
        transform = self.gameObject.transform
        transform.position.y += direction * self._speed * delta_time

        # Clamp så player ikke kan bevæge sig udenfor skærmens grænser
        # sprite_height = self.gameObject.get_component("SpriteRenderer").sprite_image.get_height()
        if transform.position.y < 0:
            transform.position.y = 0
        elif transform.position.y > self._screen_height - self._sprite_height:
            transform.position.y = self._screen_height - self._sprite_height
        
        #Shoot
        self._time_since_last_shot += delta_time
        if keys[pygame.K_SPACE] and self._time_since_last_shot >= self._shoot_cooldown:
            self.shoot()
            self._time_since_last_shot = 0

        print(self._entity.health)

    def shoot(self):
                
        pos = self.gameObject.transform.position + pygame.math.Vector2(
            self._sprite_width,
            self._sprite_height // 2
        )
        self._game_world.spawn_projectile(Entities.PLAYER_PROJECTILE, pos)

    def take_damage(self, collider):
        other = collider.gameObject
        match other._entity_type:
            case Entities.PLAYER_PROJECTILE:
                return
            case Entities.ENEMY_PROJECTILE:
                self._entity.health -= other._damage
                self._game_world._projectile_pool.return_object(other)
                self._game_world._sound_manager.play_sound(SFX.EGG_SMASH)
            case Entities.FIREBALL:
                self._entity.health -= other._damage
                self._game_world._projectile_pool.return_object(other)
        if self._entity.health <= 0:
            self._game_world._sound_manager.play_sound(SFX.PLAYER_TAKES_DAMAGE)
            self._game_world._events[GameEvents.PLAYER_DEATH](self.gameObject)

    def enemy_escaped(self):
        self._entity.health -= 1
        if self._entity.health <= 0:
            self._game_world._sound_manager.play_sound(SFX.PLAYER_TAKES_DAMAGE)
            self._game_world._events[GameEvents.PLAYER_DEATH](self.gameObject)