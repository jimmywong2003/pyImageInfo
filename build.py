#!/usr/bin/env python3
"""
PyInstaller build script for pyImageInfo
Creates a standalone executable for Windows
"""

import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Build the standalone executable using PyInstaller"""
    
    # Clean up previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # PyInstaller configuration
    pyinstaller_args = [
        'src/main.py',
        '--name=pyImageInfo',
        '--windowed',  # No console window
        '--onefile',   # Single executable
        # '--icon=assets/icon.ico',  # Commented out until icon is created
        '--add-data=src/image_processor.py;.',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ExifTags',
        '--hidden-import=PIL.ImageQt',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--clean',  # Clean PyInstaller cache
    ]
    
    print("Building standalone executable...")
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("Build completed! Executable is in the 'dist' folder.")

def create_icon():
    """Create a simple icon if one doesn't exist"""
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    icon_path = os.path.join(assets_dir, 'icon.ico')
    if not os.path.exists(icon_path):
        print("Note: No icon found. Using default PyInstaller icon.")
        # You can create a proper icon later using tools like:
        # - GIMP or Photoshop to create .ico files
        # - Online icon generators
        # - Convert PNG to ICO using PIL

if __name__ == '__main__':
    create_icon()
    build_executable()
