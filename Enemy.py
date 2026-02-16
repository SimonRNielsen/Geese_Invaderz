from Components import Entity
from Enums import Entities, Components, Collisions
from abc import ABC, abstractmethod
import pygame

class Enemy(Entity):

    def __init__(self):
        self._strategy = None
        super().__init__()

    def set_value(self, entity_type):
        self._gameObject._entity_type = entity_type
        self._damage = 1
        match entity_type:
            case Entities.GOOSIFER:
                self._speed = 400
                self._strategy = Boss_Strategy()
                self._max_health = 25
            case Entities.AGGRO_GOOSE:
                self._speed = 500
                self._strategy = Move_Strategy()
                self._max_health = 4
            case Entities.WALKING_GOOSE:
                self._speed = 300
                self._strategy = Move_Strategy()
                self._max_health = 2
            case Entities.SHEEP:
                self._speed = 300
                self._strategy = Move_Strategy(True)
                self._max_health = 2
            case _:
                self._max_health = 1
                self._speed = 100

    def awake(self, game_world):
        self._game_world = game_world
        if not self._strategy == None:
            self._strategy.enter(self, game_world)
        self._gameObject._health = self._max_health
        self._gameObject._is_destroyed = False
    
    def start(self):
        collider = self.gameObject.get_component(Components.COLLIDER.value)
        collider.subscribe(Collisions.PIXEL_ENTER, self.take_damage)

    def update(self, delta_time):
        if self._strategy is not None:
            self._strategy.execute(delta_time)

    def take_damage(self, collider):
        other = collider.gameObject
        match other._entity_type:
            case Entities.FIREBALL: #ændre til PLAYER_PROJECTILE
                self.gameObject._health -= other._damage
                other.destroy() #til object pool?
                if self.gameObject._health <= 0:
                    self._game_world._enemy_pool.return_object(self._gameObject)
            case Entities.PLAYER:
                self._game_world._enemy_pool.return_object(self._gameObject)
                other._health -= self._damage

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
        self._game_world = game_world
        if self._vertical:
            sr = self._parent.gameObject.get_component(Components.SPRITERENDERER.value)
            self._sprite_height = sr.sprite_image.get_height()

    def execute(self, delta_time):
        self._parent._gameObject.transform.position -= self._direction * self._parent.speed * delta_time
        if self._vertical:
            self._time_since_direction_change += delta_time
            if (self._parent._gameObject.transform.position.y <= 0 or self._parent._gameObject.transform.position.y >= (self._game_world.screen.get_height() - self._sprite_height)) and self._time_since_direction_change > 1:
                self._direction = -self._direction
                self._time_since_direction_change = 0
        
    def exit(self):
        pass

class Boss_Strategy(Strategy):

    def __init__(self):
        super().__init__()
        self._waypoints = []

    def enter(self, parent, game_world):
        self._parent = parent
        self._game_world = game_world
        sr = self._parent.gameObject.get_component(Components.SPRITERENDERER.value)
        self._right_border = game_world.screen.get_width() - sr.sprite_image.get_width()
        self._bottom_border = game_world.screen.get_height() - sr.sprite_image.get_height()
        self.set_waypoints()
        self._current_waypoint = self._waypoints[len(self._waypoints)-1]

    def execute(self, delta_time):
        self._parent.gameObject.transform.position += (self._parent.gameObject.transform.position - self._current_waypoint) * self._parent._speed * delta_time

    def exit(self):
        pass

    def set_waypoints(self):
        right = self._right_border
        bottom = self._bottom_border
        waypoints = self._waypoints

        waypoints.append(pygame.math.Vector2((right / 100) * 88, (bottom / 100) * 55))
        waypoints.append(pygame.math.Vector2((right / 100) * 62, (bottom / 100) * 35))
        waypoints.append(pygame.math.Vector2((right / 100) * 88, (bottom / 100) * 35))
        waypoints.append(pygame.math.Vector2((right / 100) * 62, (bottom / 100) * 55))
        waypoints.append(pygame.math.Vector2((right / 100) * 25, (bottom / 100) * 15))