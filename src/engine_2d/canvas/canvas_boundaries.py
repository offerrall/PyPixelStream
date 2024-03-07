from ..source import Source


def source_on_canvas_boundaries(source: Source,
                                canvas_size: tuple[int, int]
                                ) -> dict[str, tuple[int, int]]:

    x_position, y_position = int(source.x), int(source.y)
    width, height = source.width, source.height

    x_start_canvas = max(0, min(x_position, canvas_size[0]))
    y_start_canvas = max(0, min(y_position, canvas_size[1]))
    source_start_on_canvas = (x_start_canvas, y_start_canvas)

    x_end_canvas = max(0, min(x_position + width, canvas_size[0]))
    y_end_canvas = max(0, min(y_position + height, canvas_size[1]))
    source_end_on_canvas = (x_end_canvas, y_end_canvas)

    visible_x_start = max(0, -x_position)
    visible_y_start = max(0, -y_position)
    visible_source_start = (visible_x_start, visible_y_start)

    visible_x_end = min(width, canvas_size[0] - x_position)
    visible_y_end = min(height, canvas_size[1] - y_position)
    visible_source_end = (visible_x_end, visible_y_end)

    return {
        "source_start_on_canvas": source_start_on_canvas,
        "source_end_on_canvas": source_end_on_canvas,
        "visible_source_start": visible_source_start,
        "visible_source_end": visible_source_end
    }
