#!/usr/bin/env python2

import os
import glob
import sys

import pygame.mixer
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.escape

class SoundHandler(tornado.web.RequestHandler):
    def initialize(self, sounds):
        self.sounds = sounds


class SoundList(SoundHandler):
    def get(self):
        self.write(tornado.escape.json_encode(self.sounds.keys()))


class SoundVolume(SoundHandler):
    def get(self, sound):
        volume = self.get_argument('vol', None)
        if volume is not None and 0.0 <= float(volume) <= 1.0:
            self.sounds[sound].set_volume(float(volume))

        self.write(tornado.escape.json_encode(self.sounds[sound].get_volume()))

class SoundPlay(SoundHandler):
    def get(self, sound):
        self.sounds[sound].play(loops=-1)

class SoundStop(SoundHandler):
    def get(self, sound):
        self.sounds[sound].stop()


def main(argv=sys.argv[1:]):
    tornado.log.enable_pretty_logging()

    pygame.mixer.init()

    sounds = {}
    filenames = glob.glob('../sounds/*.ogg')
    for filename in filenames:
        key = os.path.basename(filename).rstrip('.ogg')
        sounds[key] = pygame.mixer.Sound(filename)

    try:
        app = tornado.web.Application([
            (r"/sounds", SoundList, dict(sounds=sounds)),
            (r"/sound/([^/]*)", SoundVolume, dict(sounds=sounds)),
            (r"/sound/([^/]*)/play", SoundPlay, dict(sounds=sounds)),
            (r"/sound/([^/]*)/stop", SoundStop, dict(sounds=sounds)),
            ])

        app.listen(8888)

        tornado.ioloop.IOLoop.instance().start()
    except (SystemExit, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
