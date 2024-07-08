import json
from abc import ABC

from uroboros.cli.updater_commands.fileupdater import FileUpdater


class JsonUpdater(FileUpdater, ABC):
    def __init__(self):
        super().__init__()
        self._file = None
        self._dict_tracker = None

    def _get_data(self, file):
        try:
            self._file = open(file)
        except Exception as ex:
            print(ex)
            self._error("getting data.")

        try:
            self._dict_tracker = json.load(self._file)
        except json.JSONDecodeError as ex:
            print(ex)
            self._error("getting the data dictionary.")
        return self._dict_tracker
