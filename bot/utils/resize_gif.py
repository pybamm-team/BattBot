from PIL import Image


# Original code - https://stackoverflow.com/a/41827681/14746647
def resize_gif(path, resize_to):
    """
    Resizes the GIF to a given length

    Parameters:
        path: str
        resize_to : tuple
    """

    all_frames = extract_and_resize_frames(path, resize_to)

    save_as = path

    all_frames[0].save(
        save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000
    )


def analyseImage(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.

    Parameters:
        path: str
    """
    im = Image.open(path)
    results = {
        "size": im.size,
        "mode": "full",
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:  # pragma: no cover
                    results["mode"] = "partial"
                    break
            im.seek(im.tell() + 1)

    except EOFError:
        pass

    im.close()

    return results


def extract_and_resize_frames(path, resize_to):
    """
    Iterate the GIF, extracting each frame and resizing them

    Parameter:
        path: str

    Returns:
        all_frames: list
    """
    mode = analyseImage(path)["mode"]

    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert("RGBA")

    all_frames = []

    try:
        while True:
            """
            If the GIF uses local colour tables, each frame will have its own
            palette. If not, we need to apply the global palette to the new
            frame.
            """
            if not im.getpalette():  # pragma: no cover
                im.putpalette(p)

            new_frame = Image.new("RGBA", im.size)

            """
            Is this file a "partial"-mode GIF where frames update a region of
            a different size to the entire image? If so, we need to construct
            the new frame by pasting it on top of the preceding frames.
            """
            if mode == "partial":  # pragma: no cover
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert("RGBA"))

            new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)

    except EOFError:
        pass

    im.close()

    return all_frames
