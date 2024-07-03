import os


class CtlError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'CtlError, this error is found while {} '.format(self.message)
        else:
            return 'CtlError'


class BaseCommand(object):
    def __init__(self):
        self._db_helper = None

    def _error(self, message):
        raise CtlError(message)

    @staticmethod
    def delete_backup_file(path):
        print("Restore: Delete temp dump")
        os.remove(path)

    def delete_schema(self, schm_name):
        try:
            print(f"{schm_name} delete..")
            sql = f"DROP SCHEMA {schm_name} CASCADE"
            self._db_helper.query(sql)
            self._db_helper.commit_conn()
        except Exception as e:
            print(e)
            self._error("deleting {} schema.".format(schm_name))

    def run(self, args):
        pass
