from abc import ABC, abstractmethod
import pygame
from Enums import Collisions, Components
from AssetLoader import AssetLoader

class Component(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._gameObject = None

    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self,value):
        self._gameObject = value

    @abstractmethod
    def awake(self, game_world):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

class Transform(Component):

    def __init__(self, position) -> None:
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,value):
        self._position = value

    def translate(self, direction):
        self._position += direction

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass

class SpriteRenderer(Component):

    def __init__(self, sprite_name) -> None:
        super().__init__()
        self._sprite = pygame.sprite.Sprite()
        self.change_sprite(sprite_name)

    @property
    def sprite_image(self):
        return self._sprite_image
    
    @sprite_image.setter
    def sprite_image(self, value):
        self._sprite_image = value

    @property
    def sprite(self):
        return self._sprite
    
    @property
    def sprite_mask(self):
        return self._sprite_mask
    
    def awake(self, game_world):
        self._game_world = game_world
        self._sprite.rect.topleft = self.gameObject.transform.position

    def start(self):
        pass

    def update(self, delta_time):
        self._sprite.rect.topleft = self._sprite.rect.topleft = (
            int(self.gameObject.transform.position.x),
            int(self.gameObject.transform.position.y)
        )
        self._game_world.screen.blit(self._sprite_image,self._sprite.rect)
        # self.draw_mask(self._game_world.screen, self._sprite_mask, self._sprite.rect)

    def change_sprite(self, sprite_name):
        self._sprite_image = AssetLoader.get_sprite(sprite_name)
        self._sprite.rect = self._sprite_image.get_rect()
        self._sprite_mask = pygame.mask.from_surface(self.sprite_image)

    def draw_mask(self, screen, mask, rect, color=(255, 0, 0)):
        mask_surface = mask.to_surface(
            setcolor=color,
            unsetcolor=(0, 0, 0, 0)
        )
        mask_surface.set_colorkey((0, 0, 0))
        screen.blit(mask_surface, rect.topleft)

    def set_sprite_image(self, image):
        self._sprite_image = image
        self._sprite.rect.size = image.get_size()
        self._sprite_mask = pygame.mask.from_surface(image)


class Animator(Component):

    def __init__(self) -> None:
        super().__init__()
        self._previous_position = None
        self._freeze_animation = False

    def play_animation(self, animation):
        self._current_animation = AssetLoader.get_animations(animation)
        self._animation_time = 0
        self._current_frame_index = 0

    def awake(self, game_world):
        self._sprite_renderer = self._gameObject.get_component(Components.SPRITERENDERER.value)

    def start(self):
        pass

    def update(self, delta_time):

        if self._previous_position == self._gameObject.transform.position or self._freeze_animation:
            return
        else:
            self._previous_position = pygame.math.Vector2(self._gameObject.transform.position.x, self._gameObject.transform.position.y)

        frame_duration = 0.1
        self._animation_time += delta_time

        if self._animation_time >= frame_duration:
            self._animation_time = 0
            self._current_frame_index += 1

            if self._current_frame_index >= len(self._current_animation):
                self._current_frame_index = 0

            self._sprite_renderer.set_sprite_image(
                self._current_animation[self._current_frame_index]
            )

class Collider(Component):

    def __init__(self) -> None:
        super().__init__()
        self._other_colliders = []
        self._other_masks = []
        self._listeners = {}

    @property
    def collision_box(self):
        return self._gameObject.get_component(
            Components.SPRITERENDERER.value
        ).sprite.rect

    @property
    def sprite_mask(self):
        return self._gameObject.get_component(
            Components.SPRITERENDERER.value
        ).sprite_mask
    
    def awake(self, game_world):
        sr = self._gameObject.get_component(Components.SPRITERENDERER.value)
        game_world.colliders.append(self)
        self._other_colliders.clear()
        self._other_masks.clear()
        self._listeners.clear()
        self._game_world = game_world
        self._sprite = self._gameObject.get_component(Components.SPRITERENDERER.value).sprite

    def start(self):
        pass

    def update(self, delta_time):
        pass

    def collision_check(self, other):
        if other.gameObject.is_destroyed:
            return

        is_rect_colliding = self.collision_box.colliderect(other.collision_box)
        is_already_colliding = other in self._other_colliders

        self._other_colliders = [
            obj for obj in self._other_colliders
            if not obj.gameObject.is_destroyed
        ]
        self._other_masks = [
            obj for obj in self._other_masks
            if not obj.gameObject.is_destroyed
        ]

        if is_rect_colliding:
            if not is_already_colliding:
                self.collision_enter(other)
                other.collision_enter(self)

            if self.check_pixel_collision(
                self.collision_box,
                other.collision_box,
                self.sprite_mask,
                other.sprite_mask
            ):
                if other not in self._other_masks:
                    self.pixel_collision_enter(other)
                    other.pixel_collision_enter(self)
            else:
                if other in self._other_masks:
                    self.pixel_collision_exit(other)
                    other.pixel_collision_exit(self)
        else:
            if is_already_colliding:
                self.collision_exit(other)
                other.collision_exit(self)
    def collision_enter(self, other):
        self._other_colliders.append(other)
        if Collisions.ENTER in self._listeners:
            self._listeners[Collisions.ENTER](other)

    def collision_exit(self, other):
        if other in self._other_colliders:
            self._other_colliders.remove(other)
        if Collisions.EXIT in self._listeners:
            self._listeners[Collisions.EXIT](other)

    def pixel_collision_enter(self, other):
        self._other_masks.append(other)
        if Collisions.PIXEL_ENTER in self._listeners:
            self._listeners[Collisions.PIXEL_ENTER](other)

    def pixel_collision_exit(self, other):
        if other in self._other_masks:
            self._other_masks.remove(other)
        if Collisions.PIXEL_EXIT in self._listeners:
            self._listeners[Collisions.PIXEL_EXIT](other)

    def check_pixel_collision(self, collision_box1, collision_box2, mask1, mask2):
        offset_x = collision_box2.x - collision_box1.x
        offset_y = collision_box2.y - collision_box1.y
        
        return mask1.overlap(mask2, (offset_x, offset_y)) is not None
    
    def subscribe(self, service, method):
        self._listeners[service] = method

class Entity(Component):

    def __init__(self):
        super().__init__()

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass