"""
Setup script for building Bungee Biker as a macOS application
Usage: python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('assets', ['assets']),
]
OPTIONS = {
    'argv_emulation': False,
    'packages': ['pygame', 'numpy'],
    'iconfile': 'assets/icon.icns',
    'plist': {
        'CFBundleName': 'Bungee Biker',
        'CFBundleDisplayName': 'Bungee Biker',
        'CFBundleGetInfoString': 'A 1:1 clone of Elasto Mania',
        'CFBundleIdentifier': 'com.bungeebiker.game',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': '2026 Bungee Biker',
        'NSHighResolutionCapable': True,
    },
    'optimize': 2,
}

setup(
    name='Bungee Biker',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['pygame', 'numpy'],
)
