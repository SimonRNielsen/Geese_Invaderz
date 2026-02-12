from enum import Enum, auto

class Collisions(Enum):
    ENTER = auto()
    EXIT = auto()
    PIXEL_ENTER = auto()
    PIXEL_EXIT = auto()

class Components(Enum):
    SPRITERENDERER = "SpriteRenderer"
    COLLIDER = "Collider"
    ANIMATOR = "Animator"
    ENEMY = "Enemy"

class Assets(Enum):
    START_MENU = "Start"
    BUTTON = "Button"
    BUTTON_PRESSED = "Button pressed"

class Entities(Enum):
    PLAYER = "Player"
    WALKING_GOOSE = "Walking_Goose"
    AGGRO_GOOSE = "Aggro_Goose"
    GOOSIFER = "Goosifer"
    FIREBALL = "Fireball"
    SHEEP = "Sheep"
    UNKNOWN = ""