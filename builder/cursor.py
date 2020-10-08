#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import shutil
from os import path, listdir, rename, remove, makedirs

from .config import ConfigProvider
from clickgen import build_x11_cursor_theme, build_cursor_theme, build_win_cursor_theme


class CursorBuilder():
    """
        Bibata cursors builder 🚀
    """

    def __init__(self, name: str, config: ConfigProvider):
        self.__config = config
        self.__name = name
        self.__x11_out = name
        self.__windows_out = name + "-" + "Windows"
        self.__temp_out_dir = tempfile.mkdtemp()

    def __window_bundle(self, win_theme_dir: str):
        # Remove & Rename cursors
        # If Key found => Rename else Remove
        for cursor in listdir(win_theme_dir):
            old_path = path.join(win_theme_dir, cursor)

            try:
                new_path = path.join(
                    win_theme_dir, self.__config.windows_cursors[cursor])
                rename(old_path, new_path)
            except KeyError:
                remove(old_path)

        # creating install.inf file
        install_inf_path = path.join(win_theme_dir, "install.inf")
        content = self.__config.get_windows_script(
            theme_name=self.__name, author="Kaiz Khatri")

        with open(install_inf_path, "w") as file:
            file.write(content)

    def __pack_win(self):
        win_out_dir = path.join(self.__config.out_dir, self.__windows_out)
        cur_dir = path.join(self.__temp_out_dir, self.__name, "win")

        src = path.abspath(cur_dir)
        dest = path.abspath(win_out_dir)
        shutil.move(src, dest)

        # create install.inf file in Windows Theme
        self.__window_bundle(win_theme_dir=dest)

    def __pack_x11(self):
        x11_out_dir = path.join(self.__config.out_dir, self.__x11_out)
        cur_dir = path.join(self.__temp_out_dir, self.__name, "x11")

        src = path.abspath(cur_dir)
        dest = path.abspath(x11_out_dir)
        shutil.move(src, dest)

    def build_x11_cursors(self):
        print('🌈 Building %s Theme ...' % self.__name)
        build_x11_cursor_theme(
            name=self.__name,
            image_dir=self.__config.bitmaps_dir,
            cursor_sizes=self.__config.sizes,
            hotspots=self.__config.hotspots,
            out_path=self.__temp_out_dir,
            archive=False,
            delay=self.__config.delay
        )
        self.__pack_x11()

    def build_win_cursors(self):
        print('🌈 Building %s Theme ...' % self.__name)
        build_win_cursor_theme(
            name=self.__name,
            image_dir=self.__config.bitmaps_dir,
            cursor_sizes=self.__config.sizes,
            hotspots=self.__config.hotspots,
            out_path=self.__temp_out_dir,
            archive=False,
            delay=self.__config.delay
        )
        self.__pack_win()

    def build_cursors(self):
        print('🌈 Building %s Theme ...' % self.__name)
        build_cursor_theme(
            name=self.__name,
            image_dir=self.__config.bitmaps_dir,
            cursor_sizes=self.__config.sizes,
            hotspots=self.__config.hotspots,
            out_path=self.__temp_out_dir,
            archive=False,
            delay=self.__config.delay
        )
        self.__pack_x11()
        self.__pack_win()
