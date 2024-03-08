from numpy import ndarray, flip, arange, ix_, uint8, frombuffer, where
from kivy.uix.image import CoreImage

def kivy_read_image(image_path: str,
                    alpha: bool = False
                    ):
    """
    Read an image using kivy and return it as a numpy array.
    You could use pil for this, but this way you keep the core engine with just numpy and kivy.
    """
    core_image = CoreImage(image_path)
    texture = core_image.texture
    return texture_to_np_array(texture, alpha)

def convert_bgra_to_rgb(frame_bgra):
    frame_rgb = frame_bgra[:, :, [2, 1, 0]]
    return frame_rgb

def texture_to_np_array(texture,
                        alpha: bool = False
                        ):
    size = texture.width, texture.height
    rgba_image = frombuffer(texture.pixels, dtype=uint8).reshape(size[1], size[0], 4)
    
    rgb_image = rgba_image[:, :, :3]

    if not alpha:
        return rgb_image, None

    alpha_channel = rgba_image[:, :, 3]
    alpha_mask = where(alpha_channel > 0, 1, 0)

    return rgb_image, alpha_mask

def invert_image(image: ndarray, vertical: bool = False) -> ndarray:
    if vertical:
        return flip(image, axis=0)

    return flip(image, axis=1)

def resize_mask_nearest_neighbor(mask: ndarray, new_width: int, new_height: int) -> ndarray:
    """
    This function resizes a mask using the nearest neighbor algorithm.
    """
    height, width = mask.shape

    x_scale = width / new_width
    y_scale = height / new_height

    x_indices = (arange(new_width) * x_scale).astype(int)
    y_indices = (arange(new_height) * y_scale).astype(int)

    resized_mask = mask[ix_(y_indices, x_indices)]

    return resized_mask

def nearest_neighbor_resize_vectorized(image: ndarray,
                                       new_width: int,
                                       new_height: int) -> ndarray:
    """
    This function resizes an image using the nearest neighbor algorithm.
    """
    height, width, channels = image.shape

    x_scale = width / new_width
    y_scale = height / new_height

    x_indices = (arange(new_width) * x_scale).astype(int)
    y_indices = (arange(new_height) * y_scale).astype(int)

    resized_image = image[ix_(y_indices, x_indices)]

    return resized_image