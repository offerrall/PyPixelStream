import os
import sys
from kivy.lang import Builder

# load all classes from python files for the kv files
from uix.main.content import Content
from uix.main.item_nav_bar import ItemNavBar
from uix.main.nav_bar import NavBar
from config.images import images
from uix.image_button import ImageButton

def load_kv_files():
    folder_kv_files = './kv_files/'
    path_program = sys.argv[0]
    path_program = os.path.dirname(path_program)
    folder_kv_files = os.path.join(path_program, folder_kv_files)
    for root, dirs, files in os.walk(folder_kv_files):
        for file in files:
            if file.endswith('.kv'):
                try:
                    kv_file_path = os.path.join(root, file)
                    Builder.load_file(kv_file_path)
                except Exception as e:
                    print(e)