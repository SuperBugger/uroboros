import os
import xml.etree.ElementTree as ET
from abc import ABC
from datetime import datetime

from uroboros.cli.updater_commands.fileupdater import FileUpdater


class XmlUpdater(FileUpdater, ABC):
    def __init__(self):
        super().__init__()
        self._root = None

    @staticmethod
    def unzip(zz):
        cmd = f'unzip {zz}'
        os.system(cmd)
        print(datetime.now(), "Unzip")

    def _get_data(self, path):
        try:
            self.unzip(path)
            tree = ET.parse("export/export.xml")
            self._root = tree.getroot()
        except Exception as e:
            print(e)
            self._error("getting data. {}")

    def _clear_trash(self):
        super()._clear_trash()
        try:
            print(datetime.now(), "Delete temporary directory for zip")
            cmd = 'rm -fr export'
            os.system(cmd)
        except Exception as e:
            print(e)
            self._error("deleting temporary directory for zip.")
