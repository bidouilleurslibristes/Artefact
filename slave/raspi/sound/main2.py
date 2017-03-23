import pyglet

pyglet.options['audio'] = ('pulse', 'openal', 'silent')

music = pyglet.media.load("./sample.mp3")

player = pyglet.media.Player()

player.queue(music)

player.play()
player.volume = 1
pyglet.app.run()