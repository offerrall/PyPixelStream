import os
import subprocess
import shutil

def create_exe():
    main_script = './src/main.py'
    folders_to_add = [
        './src/config',
        './src/kv_files',
    ]
    
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--hidden-import=plyer.platforms.win.filechooser',
        main_script
    ]

    subprocess.call(pyinstaller_cmd)

    folder_out = './dist/'

    for folder in folders_to_add:
        _folder_name = folder.split('/')[-1]
        _folder_out = folder_out + '/' + _folder_name
        shutil.copytree(folder, _folder_out)

    # remove all .py fles from ./src/config
    for file in os.listdir(folder_out + '/config'):
        if file.endswith('.py'):
            os.remove(folder_out + '/config/' + file)

    shutil.rmtree('./build')
    os.remove('./main.spec')


if __name__ == '__main__':
    create_exe()
