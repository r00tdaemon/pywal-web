def get_brightness(_, rgb: str):
    # http://www.w3.org/TR/AERT#color-contrast
    rgb = rgb.strip("#")
    rgb = int(rgb, 16)
    r = (rgb >> 16) & 0xff
    g = (rgb >> 8) & 0xff
    b = rgb & 0xff
    return (r * 299 + g * 587 + b * 114) / 1000


def is_dark(_, rgb: str):
    return get_brightness(_, rgb) < 128
