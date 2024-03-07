from art import text2art
from numpy import ndarray, full, uint8, zeros

_fonts = """xtimes
xsans
xsansi
morse
xttyb
heroboti
home_pak
house_of
hyper
inc_raw
italics
kgames
dic_4x4
c_ascii
fraktur
funface
georgi16
impossible
jacky
merlin1
modular
nscript
smpoison
soft
stacey
stampate
sweet"""

def get_fonts() -> list[str]:
    return _fonts.split()

def convert_text_to_image(text: str,
                          font: str,
                          text_color: tuple[int, int, int],
                          background_color: tuple[int, int, int] | None = None) -> tuple[ndarray, ndarray]:
    """
    Convert the given text to an image with the given font and colors.
    the image will be returned as a numpy array with the given text color and the background color.
    if the background color is None, the image will have a transparent background.

    Returns a tuple with the image and the mask for the text.
    """
    ascii_art = text2art(text, font)

    # Clean up the ascii art
    ascii_lines = ascii_art.split("\n")
    num_columns = max(len(line) for line in ascii_lines)
    col_index_start, col_index_end = 0, num_columns

    # Find the start and end of the ascii art
    for col_index in range(num_columns):
        if any(len(line) > col_index and line[col_index] != ' ' for line in ascii_lines):
            col_index_start = col_index
            break
    
    # Find the end of the ascii art
    for col_index in range(num_columns-1, -1, -1):
        if any(len(line) > col_index and line[col_index] != ' ' for line in ascii_lines):
            col_index_end = col_index
            break
    
    # Remove leading and trailing spaces
    cleaned_ascii = "\n".join([line[col_index_start:col_index_end+1] for line in ascii_lines if not all(char == ' ' for char in line)])
    ascii_lines = cleaned_ascii.split('\n')
    height, width = len(ascii_lines), max(len(line) for line in ascii_lines)

    # Create the image
    fill = (0, 0, 0) if background_color is None else background_color
    image = full((height, width, 3), fill, dtype=uint8)

    # Create the mask for the text
    mask = zeros((height, width), dtype=bool)
    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line):
            if char != ' ':
                image[y, x] = text_color
                mask[y, x] = True

    if background_color is not None:
        mask = None

    return image, mask


def set_text_to_frame(text: str,
                      frame: ndarray | None,
                      mask: ndarray | None,
                      font: str,
                      text_color: tuple[int, int, int],
                      background_color: tuple[int, int, int] | None = None) -> None:
    """
    This applies the given text to the given frame, not creating a new image as convert_text_to_image does.
    """

    text_image, text_mask = convert_text_to_image(text, font, text_color, background_color)
    cut1 = text_image.shape[0]
    cut2 = text_image.shape[1]

    if cut1 > frame.shape[0]:
        cut1 = frame.shape[0]
    
    if cut2 > frame.shape[1]:
        cut2 = frame.shape[1]
    
    frame[:cut1, :cut2] = text_image[:cut1, :cut2]
    if mask is not None:
        mask[:cut1, :cut2] = text_mask[:cut1, :cut2]