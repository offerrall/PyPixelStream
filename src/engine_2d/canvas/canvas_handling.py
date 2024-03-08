from numpy import ndarray, where

from ..source import Source
from .canvas_boundaries import source_on_canvas_boundaries


def get_source_at_position(sources: list[Source],
                           position: tuple[int, int],
                           canvas_size: tuple[int, int]) -> Source | None:
    """
    This function returns the source at the given position. if there is no source at the given position it returns None.
    Its used to get the source that is being clicked on the canvas by the user.
    """
    x, y = position
    sources = sorted(sources, key=lambda source: source.order, reverse=True)

    for source in sources:
        if not source.is_visible or source.is_selectable:
            continue

        source_boundaries = source_on_canvas_boundaries(source, canvas_size)
        ss = source_boundaries["source_start_on_canvas"]
        se = source_boundaries["source_end_on_canvas"]

        if ss[0] <= x <= se[0] and ss[1] <= y <= se[1]:
            return source

    return None

def apply_mask_to_background(background: ndarray,
                             frame: ndarray,
                             mask: ndarray,
                             sYs: slice,
                             sXs: slice,
                             cYs: slice,
                             cXs: slice):
    """
    This function applies a mask to a frame.
    the mask is used to apply the frame to the background only in the areas where the mask is True.
    """
    mask = mask[sYs, sXs]
    try:
        background[cYs, cXs] = where(mask[..., None],
                                        frame[sYs, sXs],
                                        background[cYs, cXs])
    except ValueError:
        print("Error applying mask to background")

def apply_source_to_background(background: ndarray,
                               source: Source,
                               frame: ndarray,
                               mask: ndarray | None = None):
    """
    This function applies a source to a background.
    It applies the source to the background only in the areas where the source is visible.
    """

    canvas_size = (background.shape[1], background.shape[0])
    source_boundaries = source_on_canvas_boundaries(source, canvas_size)

    sYs = slice(source_boundaries["visible_source_start"][1],
                source_boundaries["visible_source_end"][1])
    sXs = slice(source_boundaries["visible_source_start"][0],
                source_boundaries["visible_source_end"][0])
    cYs = slice(source_boundaries["source_start_on_canvas"][1],
                source_boundaries["source_end_on_canvas"][1])
    cXs = slice(source_boundaries["source_start_on_canvas"][0],
                source_boundaries["source_end_on_canvas"][0])

    if sYs.start >= sYs.stop or sXs.start >= sXs.stop:
        return

    has_mask = mask is not None

    if has_mask:
        apply_mask_to_background(background, frame, mask, sYs, sXs, cYs, cXs)
        return

    try:
        background[cYs, cXs] = frame[sYs, sXs]
    except ValueError:
        print("Error applying source to background")

