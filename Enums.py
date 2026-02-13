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
    WIN_SCREEN = "Win"
    LOOSE_SCREEN = "Loose"
    BUTTON = "Button"
    BUTTON_PRESSED = "Button pressed"
    PAUSE = "Pause"

class Entities(Enum):
    PLAYER = "Player"
    WALKING_GOOSE = "Walking_Goose"
    AGGRO_GOOSE = "Aggro_Goose"
    GOOSIFER = "Goosifer"
    FIREBALL = "Fireball"
    SHEEP = "Sheep"
    UNKNOWN = ""

class Button_Types(Enum):
    START = "Start"
    EXIT = "Exit"