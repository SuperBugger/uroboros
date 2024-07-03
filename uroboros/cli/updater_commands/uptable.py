"""
    Классы работы с обновлением таблицы
"""


class UpTable:
    """
    Обновляемая таблица в БД
    """

    def __init__(self, db_helper, name, fields):
        """
        :param ipbpi.postgresql.PGConnection: открытый экземпляр подключения к СУБД PostgreSQL
        :param name: Имя таблицы
        :param fields: Список имен полей
        """
        self._db_helper = db_helper
        self._name = name
        self._fields = fields
        self._stmt_name = None
        self._schm = None
        self._prepare_stmt = None
        self._insert_stmt = None
        self.clear()

    @property
    def name(self):
        return self._name

    @property
    def fields(self):
        return self._fields

    @property
    def rows(self):
        return self._rows

    def _prepare_insert(self):
        self._stmt_name = '{}_stmt'.format(self._name)
        self._prepare_stmt = '''
                PREPARE {} AS
                INSERT INTO "{}"."{}"({}) VALUES ({})
               '''.format(self._stmt_name, self._schm, self._name,
                          ', '.join(self._fields),
                          ', '.join('${}'.format(i) for i in range(1, len(self._fields) + 1)))
        self._insert_stmt = '''
                EXECUTE {} ({})'''.format(self._stmt_name,
                                          ', '.join(['%s'] * len(self._fields)))

    def insert(self, row):
        self._rows.append(row)

    def _internal_upload(self):
        for row in self._rows:
            self._db_helper.query((self._insert_stmt, row))
        self._db_helper.commit_conn()

    def upload(self):
        if not self._stmt_name:
            self._prepare_insert()
        self._db_helper.query(self._prepare_stmt)
        self._internal_upload()

    def clear(self):
        self._rows = []

    def update_field(self, field, oldval, newval):
        raise NotImplementedError()

    @property
    def rows_count(self):
        return len(self._rows)

    def _deallocate_stmt(self):
        if self._stmt_name:
            try:
                self._db_helper.query('DEALLOCATE {}'.format(self._stmt_name))
                self._db_helper.commit_conn()
            except Exception as e:
                print(e)
            finally:
                self._stmt_name = None


class UpTableKeyed(UpTable):
    """
    Обновляемая таблица с ключом в БД
    """

    def __init__(self, conn, name, fields):
        super().__init__(conn, name, fields)
        self._key2id = {}
        self._rows = {}
        self._seq = 0

    def clear(self):
        self._rows = {}
        self._seq = 0
        self._key2id = {}

    def get_max_id(self):
        return max(self._rows.keys())

    def getid(self, key):
        id = self._key2id.get(key, None)
        if not id:
            self._seq += 1
            id = self._seq
            self._key2id[key] = id
        return id

    def insert(self, row):
        raise NotImplementedError()

    def upsert(self, key, row):
        self._rows[key] = row

    def update(self, rows):
        self._rows.update(rows)

    def change_field_value(self, field, oldval, newval):
        fp = self._fields.index(field)
        if fp < 0:
            return
        for k, r in self._rows.items():
            if r[fp] == oldval:
                r[fp] = newval

    def _internal_upload(self):
        for key, row in self._rows.items():
            self._db_helper.query([self._insert_stmt, row])
        self._db_helper.commit_conn()
