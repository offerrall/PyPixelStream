
def rgb_to_kivy_color(rgb):
    rgba = [rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, 1]
    return rgba

def kivy_color_to_rgb(kivy_color):
    return [int(kivy_color[0] * 255), int(kivy_color[1] * 255), int(kivy_color[2] * 255)]

