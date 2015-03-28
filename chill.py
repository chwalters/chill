import os

import pygame.mixer
import yaml

pygame.mixer.init()


class Sound(pygame.mixer.Sound):
    def __init__(self, filename):
        filename = os.path.expanduser(filename)
        filename = os.path.expandvars(filename)
        self.sound = pygame.mixer.Sound(filename)
        self.playing = False

    def __repr__(self):
        return repr({
            'volume': self.volume,
            'playing': self.playing,
            })

    def play(self):
        self.sound.play(loops=-1)
        self.playing = True

    def stop(self):
        self.sound.stop()
        self.playing = False

    @property
    def volume(self):
        return self.sound.get_volume()

    @volume.setter
    def volume(self, volume):
        assert 0 <= volume <= 1
        self.sound.set_volume(volume)


class SoundBank(object):
    def __init__(self, sounds):
        self._sounds = sounds

    def __repr__(self):
        return repr({'sounds': self._sounds})

    def __getitem__(self, name):
        return self._sounds[name]

    @classmethod
    def load(cls, filename):
        filename = os.path.expanduser(filename)
        filename = os.path.expandvars(filename)
        with open(filename) as fp:
            config = yaml.load(fp)

        sounds = {}
        for item in config['sounds']:
            sound = Sound(item['path'])
            sound.volume = item['vol']
            sounds[item['name']] = sound

        return cls(sounds)

    @property
    def sounds(self):
        return self._sounds.keys()

    def play(self):
        for sound in self._sounds.values():
            if sound.volume > 0:
                sound.play()

    def stop(self):
        for sound in self._sounds.values():
            sound.stop()

    def sound(self, name):
        return self._sounds[name]
