from Components import Entity
from Enums import Entities, Components, Collisions, GameEvents, SFX, Music
from abc import ABC, abstractmethod
import pygame, random

class Enemy(Entity):

    def __init__(self):
        self._strategy = None
        super().__init__()

    def set_value(self, entity_type):
        self._gameObject._entity_type = entity_type
        self._sprite_width = self._gameObject.get_component(Components.SPRITERENDERER.value).sprite_image.get_width()
        self._x_left_boundary = -self._sprite_width
        match entity_type:
            case Entities.GOOSIFER:
                self._speed = 400
                self._strategy = Boss_Strategy()
                self._max_health = 25
                self._damage = 5
            case Entities.AGGRO_GOOSE:
                self._speed = 500
                self._strategy = Move_Strategy()
                self._max_health = 4
                self._damage = 3
            case Entities.WALKING_GOOSE:
                self._speed = 300
                self._strategy = Move_Strategy()
                self._max_health = 2
                self._damage = 2
            case Entities.OBERST:
                self._speed = 300
                self._strategy = Move_Strategy(True)
                self._max_health = 2
                self._damage = 1
            case _:
                self._max_health = 1
                self._speed = 100

    def awake(self, game_world):
        self._game_world = game_world
        self._gameObject._health = self._max_health
        self._gameObject._is_destroyed = False
        screen_width = game_world.screen.get_width()
        if self.gameObject._entity_type is Entities.OBERST:
            self._initial_x = random.randint(int(screen_width * 0.6),int(screen_width * 0.95))
        if not self._strategy == None:
            self._strategy.enter(self, game_world)
    
    def start(self):
        collider = self.gameObject.get_component(Components.COLLIDER.value)
        collider.subscribe(Collisions.PIXEL_ENTER, self.take_damage)
        if self.gameObject._entity_type is not Entities.OBERST:
            self._game_world._sound_manager.play_sound(SFX.ENEMY_HONK)
        else:
            self._game_world._sound_manager.play_sound(SFX.SHEEP)

    def update(self, delta_time):
        if self._strategy is not None:
            self._strategy.execute(delta_time)
        if self.gameObject.transform.position.x <= self._x_left_boundary:
            self._game_world._enemy_pool.return_object(self.gameObject)
            self._game_world._events[GameEvents.ENEMY_ESCAPED]()
        
        if self._game_world.player_alive.is_destroyed == True:
            self._gameObject.is_destroyed = True

    def take_damage(self, collider):
        other = collider.gameObject
        match other._entity_type:
            case Entities.PLAYER_PROJECTILE:
                self._game_world._sound_manager.play_sound(SFX.HVEDE)
                self.gameObject._health -= other._damage
                self._game_world._projectile_pool.return_object(other)
                if self.gameObject._health <= 0:

                    if self.gameObject._entity_type == Entities.GOOSIFER:
                        self._game_world.level_manager.boss_killed()
                        self._game_world._sound_manager.play_music(Music.MENU)

                    self._game_world._enemy_pool.return_object(self._gameObject)
            case Entities.PLAYER:
                self._game_world._enemy_pool.return_object(self._gameObject)
                other.get_component(Components.ENTITY.value).health -= self._damage

    @property
    def speed(self):
        return self._speed

class Strategy(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def enter(self, parent, game_world):
        pass

    @abstractmethod
    def execute(self, delta_time):
        pass

    @abstractmethod
    def exit(self):
        pass

class Move_Strategy(Strategy):

    def __init__(self, vertical= False):
        super().__init__()
        if vertical:
            self._direction = pygame.math.Vector2(0, 1)
            self._time_since_direction_change = 0
        else:
            self._direction = pygame.math.Vector2(1, 0)
        self._vertical = vertical

    def enter(self, parent, game_world):
        self._parent = parent
        if self._parent._strategy is not None and self._parent._strategy is not self:
            self._parent._strategy.exit()
            self._parent._strategy = self
        self._game_world = game_world
        if self._vertical:
            sr = self._parent.gameObject.get_component(Components.SPRITERENDERER.value)
            self._sprite_height = sr.sprite_image.get_height()
            self._sprite_width = sr.sprite_image.get_width()
            self._screen_height = game_world.screen.get_height()
            self._time_since_last_shot = -3
            self._can_shoot_after = 2

    def execute(self, delta_time):
        if self._vertical:
            self._time_since_direction_change += delta_time
            self._time_since_last_shot += delta_time
            if self._time_since_last_shot >= self._can_shoot_after:
                self.shoot()
            x_distance = abs(self._parent._initial_x - self._parent._gameObject.transform.position.x)
            if x_distance > 60:
                self._parent._gameObject.transform.position -= pygame.math.Vector2(1,0) * self._parent.speed * delta_time
                return
            if (self._parent._gameObject.transform.position.y <= 0 or self._parent._gameObject.transform.position.y >= (self._screen_height - self._sprite_height)) and self._time_since_direction_change > 1:
                self._direction = -self._direction
                self._time_since_direction_change = 0
        self._parent._gameObject.transform.position -= self._direction * self._parent.speed * delta_time
        
    def exit(self):
        self._parent._previous_strategy = self

    def shoot(self):
        parent_pos = self._parent.gameObject.transform.position
        pos = pygame.math.Vector2(parent_pos.x, parent_pos.y + (self._sprite_height / 2))
        self._game_world.spawn_projectile(Entities.ENEMY_PROJECTILE, pos)
        self._time_since_last_shot = 0

class Boss_Strategy(Strategy):

    def __init__(self):
        super().__init__()
        self._waypoints = []
        self._first_shot = False
        self._second_shot = False
        self._time_since_last_barrage = -2
        self._time_between_barrages = 5

    def enter(self, parent, game_world):
        self._parent = parent
        if self._parent._strategy is not None and self._parent._strategy is not self:
            self._parent._strategy.exit()
            self._parent._strategy = self
        self._game_world = game_world
        sr = self._parent.gameObject.get_component(Components.SPRITERENDERER.value)
        self._sprite_height = sr.sprite_image.get_height()
        self._sprite_width = sr.sprite_image.get_width()
        self._right_border = game_world.screen.get_width() - self._sprite_width
        self._bottom_border = game_world.screen.get_height() - self._sprite_height
        self.set_waypoints()
        self._current_waypoint = self._waypoints[len(self._waypoints)-1]

    def execute(self, delta_time):
        self._game_world._sound_manager.play_music(Music.BOSSFIGHT)
        self._time_since_last_barrage += delta_time
        if self._time_since_last_barrage >= self._time_between_barrages:
            self.shoot()
        direction = self._current_waypoint - self._parent.gameObject.transform.position
        if direction.length() < 10:
            self._current_waypoint = self._waypoints.pop(0)
            self._game_world._sound_manager.play_sound(SFX.ENEMY_HONK)
            self._waypoints.append(self._current_waypoint)
        direction = direction.normalize()
        self._parent.gameObject.transform.position += direction * self._parent.speed * delta_time

    def exit(self):
        self._parent._previous_strategy = self

    def set_waypoints(self):
        right = self._right_border
        bottom = self._bottom_border
        waypoints = self._waypoints
        waypoints.append(pygame.math.Vector2(right * 0.75, bottom * 0.01))  # top
        waypoints.append(pygame.math.Vector2(right * 0.98, bottom * 0.98))  # nederst højre
        waypoints.append(pygame.math.Vector2(right * 0.52, bottom * 0.30))  # midt venstre
        waypoints.append(pygame.math.Vector2(right * 0.98, bottom * 0.30))  # midt højre
        waypoints.append(pygame.math.Vector2(right * 0.52, bottom * 0.98))  # nederst venstre

    def shoot(self):
        pos = self._parent.gameObject.transform.position
        shot_pos = pygame.math.Vector2(pos.x, pos.y + (self._sprite_height / 2))
        if not self._first_shot:
            self._first_shot = True
            self._game_world.spawn_projectile(Entities.FIREBALL, shot_pos)
        elif self._time_since_last_barrage >= self._time_between_barrages + 0.5 and not self._second_shot:
            self._second_shot = True
            self._game_world.spawn_projectile(Entities.FIREBALL, shot_pos)
        elif self._time_since_last_barrage >= self._time_between_barrages + 1:
            self._game_world.spawn_projectile(Entities.FIREBALL, shot_pos)
            self._time_since_last_barrage = 0
            self._first_shot = False
            self._second_shot = False
