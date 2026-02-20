from Enums import Components
from Components import Component


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
        self._gameObject._is_destroyed = False
        self._sprite_width = self.gameObject.get_component(Components.SPRITERENDERER.value).sprite_image.get_width()

    def start(self):
        pass

    def update(self, delta_time):
        #Flyt projectiles
        self._transform.position.x += self._speed * delta_time * self._direction

        #Fjern hvis udenfor skærmen
        if self._transform.position.x < -self._sprite_width or self._transform.position.x > self._screen.get_width():
            self._game_world._projectile_pool.return_object(self.gameObject)