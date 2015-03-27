#!/usr/bin/env python2

import os
import glob
import sys

import pygame.mixer
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.escape

class Sound(pygame.mixer.Sound):
    def __init__(self, filename):
        super(Sound, self).__init__(filename)
        self.playing = False

    def __repr__(self):
        return repr({
            'volume': self.get_volume(),
            'playing': self.playing,
            })

    def start(self):
        super(Sound, self).start(loops=-1)
        self.playing = True

    def stop(self):
        super(Sound, self).stop()
        self.playing = False


class SoundHandler(tornado.web.RequestHandler):
    def initialize(self, sounds):
        self.sounds = sounds


class SoundList(SoundHandler):
    def get(self):
        state = {k: str(v) for k, v in self.sounds.items()}
        self.write(tornado.escape.json_encode(state))


class SoundState(SoundHandler):
    def get(self, sound):
        volume = self.get_argument('vol', None)
        if volume is not None and 0.0 <= float(volume) <= 1.0:
            self.sounds[sound].set_volume(float(volume))

        play = self.get_argument('play', None)
        if play is not None:
            if play.lower() == 'true':
                self.sounds[sound].play()
            elif play.lower() == 'false':
                self.sounds[sound].stop()

        state = {sound: str(self.sounds[sound])}
        self.write(tornado.escape.json_encode(state))


def main(argv=sys.argv[1:]):
    tornado.log.enable_pretty_logging()

    pygame.mixer.init()

    sounds = {}
    filenames = glob.glob('../sounds/*.ogg')
    for filename in filenames:
        key = os.path.basename(filename).rstrip('.ogg')
        sounds[key] = Sound(filename)

    try:
        app = tornado.web.Application([
            (r"/sounds", SoundList, dict(sounds=sounds)),
            (r"/sound/([^/]*)", SoundState, dict(sounds=sounds)),
            ])

        app.listen(8888)

        tornado.ioloop.IOLoop.instance().start()
    except (SystemExit, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
