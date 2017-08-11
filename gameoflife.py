from gameoflife.animation import Animation
from gameoflife.imagegen import ImageGen
from gameoflife.pattern import Pattern


if __name__ == '__main__':
    pattern = Pattern('patterns/galaxy.png')
    spritepath = 'sprites/circle8.png'
    outpath = './images'
    cellsize = 40
    gencount = 8

    # generate a set of images
    # ImageGen(pattern.cells, spritepath, pattern.dims, cellsize).draw(outpath, gencount)

    # display an animation
    Animation(pattern.cells, spritepath, *pattern.dims, cellsize).run()
