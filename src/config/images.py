import sys
import os

"""
This file is used to store the path of the images used in the application.
"""

path_images = "./config/assets/images/"

path_program = sys.argv[0]
path_program = os.path.dirname(path_program)
path_images = os.path.join(path_program, path_images)

images = {}

for image in os.listdir(path_images):
    if image.endswith('.png'):
        images[image.split('.')[0]] = path_images + image

