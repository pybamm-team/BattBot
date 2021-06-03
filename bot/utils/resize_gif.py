from PIL import Image


def resize_gif(frames):
    """
    This is used to resize a GIF so that it
    can be tweeted.
    Parameters:
        frames: ImageSequence.Iterator
    Yields:
        new_gif

    Reference -
    https://gist.github.com/skywodd/8b68bd9c7af048afcedcea3fb1807966
    """

    size = 1440, 1440

    for frame in frames:
        new_gif = frame.copy()
        new_gif.thumbnail(size, Image.ANTIALIAS)
        yield new_gif
