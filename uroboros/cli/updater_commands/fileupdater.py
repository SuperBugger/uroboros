import os
from abc import ABC
from datetime import datetime

import requests as requests

from cli.updater_commands.baseupdater import Updater


class FileUpdater(Updater, ABC):
    def __init__(self):
        super().__init__()
        self._url = None
        self.name_obj = None

    def _download_obj(self, url):
        self._url = url
        self.name_obj = self._url.split("/")[-1]
        try:
            cmd = 'mkdir -p data'
            os.system(cmd)
            print(datetime.now(), "Create temporary directory")
            with open(f"data/{self.name_obj}", 'wb') as f:
                resp = requests.get(self._url, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
                f.write(resp.content)
        except Exception as e:
            print(e)
            self._error("downloading {}".format(self.name_obj))
        return self.name_obj

    def _clear_trash(self):
        try:
            print(datetime.now(), "Delete temporary directory")
            cmd = 'rm -fr data'
            os.system(cmd)
        except Exception as e:
            print(e)
            self._error("deleting temporary directory.")
