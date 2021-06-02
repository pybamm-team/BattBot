from PIL import Image


def resize_gif(frames):

    size = 1080, 1080

    for frame in frames:
        new_gif = frame.copy()
        new_gif.thumbnail(size, Image.ANTIALIAS)
        yield new_gif
