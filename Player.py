import pygame
from Enums import Entities, GameEvents, Components, Collisions, SFX
from Components import Component

class Player(Component):
    def __init__(self, speed=400):
        super().__init__()
        self._speed = speed
        self._screen_height = None
        self._shoot_cooldown = 0.50
        self._time_since_last_shot = 0

        self._projectile_type = Entities.PLAYER_PROJECTILE
        self._projectile_speed = 600
        self._projectile_damage = 1
        self._shooting = False
        self._shooting_animation_timer = 0

    @property
    def shooting(self):
        return self._shooting

    def awake(self, gameWorld):
        #Gem reference til skærmen, så der kan laves højdegrænser
        self._screen_height = gameWorld.screen.get_height()
        self._game_world = gameWorld
        self._gameObject._entity_type = Entities.PLAYER
        self._gameObject._health = 3
        self._sr = self.gameObject.get_component("SpriteRenderer")
        self._sprite_height = self._sr.sprite_image.get_height()
        self._sprite_width = self._sr.sprite_image.get_width()
        gameWorld.subscribe(GameEvents.ENEMY_ESCAPED, self.enemy_escaped)
        self._animator = self.gameObject.get_component(Components.ANIMATOR.value)

    def start(self):
        collider = self.gameObject.get_component(Components.COLLIDER.value)
        collider.subscribe(Collisions.PIXEL_ENTER, self.take_damage)
        self._entity = self.gameObject.get_component("Entity")
            
    def update(self, delta_time):
        if self.gameObject is None:
            return
        
        if self._shooting:
            self._shooting_animation_timer += delta_time
            if self._shooting_animation_timer >= 0.3:
                self._shooting = False
                self._shooting_animation_timer = 0
                self._animator._freeze_animation = False
                self._sr.change_sprite(Entities.PLAYER)
        
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


    def apply_level_modifiers(self, modifiers: dict) :
        #if "speed" in modifiers:
        self._speed = modifiers.get("speed", self._speed)
        #if "shoot_cooldown" in modifiers:
        self._shoot_cooldown = modifiers.get("shoot_cooldown", self._shoot_cooldown)
        #if "projectile_type" in modifiers:
        self._projectile_type = modifiers.get("projectile_type", self._projectile_type)
        #if "projectile_speed" in modifiers:
        self._projectile_speed = modifiers.get("projectile_speed", self._projectile_speed)
        #if "projectile_damage" in modifiers:
        self._projectile_damage = modifiers.get("projectile_damage", self._projectile_damage)
        
        self._game_world._projectile_pool.upgrade_pooled_shots(self._projectile_type, self._projectile_damage)

    def shoot(self):
        self._animator._freeze_animation = True
        self._shooting = True
        self._sr.change_sprite(Entities.PLAYER_SHOOTING)
        pos = self.gameObject.transform.position + pygame.math.Vector2(
            self._sprite_width,
            self._sprite_height // 2
        )
        self._game_world.spawn_projectile(Entities.PLAYER_PROJECTILE, pos)

    def take_damage(self, collider):
        other = collider.gameObject
        match other._entity_type:
            case Entities.ENEMY_PROJECTILE:
                self._entity.health -= other._damage
                self._game_world._projectile_pool.return_object(other)
                self._game_world._sound_manager.play_sound(SFX.EGG_SMASH)
            case Entities.FIREBALL:
                self._entity.health -= other._damage
                self._game_world._projectile_pool.return_object(other)
                self._game_world._sound_manager.play_sound(SFX.FIRE_HIT)
        self._game_world._sound_manager.play_sound(SFX.PLAYER_TAKES_DAMAGE)
        if self._entity.health <= 0:
            self._game_world._events[GameEvents.PLAYER_DEATH](self.gameObject)

    def enemy_escaped(self):
        self._entity.health -= 1
        self._game_world._sound_manager.play_sound(SFX.PLAYER_TAKES_DAMAGE)
        if self._entity.health <= 0:
            self._game_world._events[GameEvents.PLAYER_DEATH](self.gameObject)