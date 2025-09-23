
# setup.py

# using cx_freeze from
# https://github.com/sekrause/cx_Freeze-Wheels
# May 2016

# docs: http://cx-freeze.readthedocs.io/en/latest/distutils.html


from cx_Freeze import setup, Executable
import os

# print(os.environ['LOCALAPPDATA'])
pygamePath = os.environ['LOCALAPPDATA'] + \
                 "\\Programs\\Python\\Python35-32\\Lib\\site-packages\\pygame\\"
# print(pygamePath)



shortcut_table = [
    ("Invaders",               # Shortcut
     "DesktopFolder",          # Directory_
     "Invaders",               # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]\invaders.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",               # WkDir
     )
    ]
 
msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {'initial_target_dir': r'[DesktopFolder]\invaders',
                     'data': msi_data}

target = Executable(
    script = "invaders.py",
    base = 'Win32GUI',
    icon = "Apathae-Satellite-2-Games.ico",    # from http://www.iconarchive.com/
  )


setup(
    name="Invaders",
    author = "Andrew Davison",
    version = "0.1",
    description = "Simple Space Invaders clone",

    options={
      "build_exe": {     # build_exe_options
         "packages":["pygame"],

         "excludes": ["tkinter", "tcl", "numpy"],

         # "optimize": 2,

         "silent": True,

         "include_files":["Orbitracer.ttf",
                "startScreen.jpg", "background.jpg", 
                "player.png", "alien.png", 
                "alienExploSheet.png", "exploSheet.png",
                "arpanauts.ogg", 
                "boom.wav", "explode.wav", "fire.wav",  
               (pygamePath+"libogg.dll", "libogg.dll"),
               (pygamePath+"libvorbis.dll",  "libvorbis.dll"),
               (pygamePath+"libvorbisfile.dll", "libvorbisfile.dll"),
              ]          # force cx_freeze to include OGG DLLs from Pygame

      },

      "bdist_msi": bdist_msi_options,

    },

    executables = [target]
)



