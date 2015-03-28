#!/usr/bin/env python2

import sys

import tornado.ioloop
import tornado.web
import tornado.log
import tornado.escape

import chill


class SoundHandler(tornado.web.RequestHandler):
    def initialize(self, sound_bank):
        self.sound_bank = sound_bank


class SoundList(SoundHandler):
    def get(self):
        self.write(tornado.escape.json_encode(self.sound_bank.sounds))


class SoundState(SoundHandler):
    def get(self, sound):
        volume = self.get_argument('vol', None)
        if volume is not None:
            self.sound_bank[sound].volume = float(volume)

        play = self.get_argument('play', None)
        if play is not None:
            if play.lower() == 'true':
                self.sound_bank[sound].play()
            elif play.lower() == 'false':
                self.sound_bank[sound].stop()

        state = {sound: str(self.sound_bank[sound])}
        self.write(tornado.escape.json_encode(state))


def main(argv=sys.argv[1:]):
    tornado.log.enable_pretty_logging()

    sound_bank = chill.SoundBank.load('chill.yaml')

    try:
        app = tornado.web.Application([
            (r"/sounds", SoundList, dict(sound_bank=sound_bank)),
            (r"/sound/([^/]*)", SoundState, dict(sound_bank=sound_bank)),
            ])

        app.listen(8888)

        tornado.ioloop.IOLoop.instance().start()
    except (SystemExit, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
