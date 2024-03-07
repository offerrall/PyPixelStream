def _get_color(colors: dict[str, tuple[int, int, int, int]],
               name: str) -> tuple[float, float, float, float]:
    color = colors[name]
    return_color = []

    for value in color:
        return_color.append(value / 255)
    
    return tuple(return_color)

def _init_colors(colors: dict[str, tuple[int, int, int, int]]) -> None:
    for key in colors:
        colors[key] = _get_color(colors, key)

colors = {}

colors["background"] = 16, 16, 16, 255
colors["secundary_background"] = 34, 34, 34, 255
colors["font"] = 255, 255, 255, 255
colors["selected"] = 255, 0, 0, 255
colors["separate"] = 120, 120, 120, 255
colors["none"] = 0, 0, 0, 0


_init_colors(colors)
