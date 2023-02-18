import os
import shutil
import unittest
import uuid
import pyodbc
from ..pyodbc_helpers import *


class Test_pyodbc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        shutil.rmtree(cls.fix_tmproot())

    @staticmethod
    def fix_tmproot():
        return os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp'))

    def setUp(self):
        self._dbc = None
        self._tmpdir = None

    def fix_tmpdir(self):
        if self._tmpdir is not None:
            return self._tmpdir
        self._tmpdir = os.path.join(self.fix_tmproot(), uuid.uuid4().hex)
        os.makedirs(self._tmpdir, exist_ok=True)
        return self._tmpdir

    def fix_dbc(self):
        if self._dbc is not None:
            return self._dbc
        db_path = os.path.join(self.fix_tmpdir(), 'db.sqlite')
        dbc = pyodbc.connect(f"Driver=SQLite3 ODBC Driver;Database={db_path}")
        with dbc.cursor() as c:
            c.execute('CREATE TABLE users (id INT, name VARCHAR(128))')
            c.executemany('INSERT INTO users (id, name) VALUES (?,?)', [(1, 'John'), (2, 'Jane')])
            c.commit()
        return dbc

    def test_connect(self):
        dbc = self.fix_dbc()

    def test_fetchall(self):
        dbc = self.fix_dbc()
        with dbc.cursor() as c:
            c.execute('SELECT id, name FROM users ORDER BY id')
            rows = c.fetchall()
        self.assertEqual([(1, 'John'),(2, 'Jane')], [tuple(r) for r in rows])


    def test_description(self):
        dbc = self.fix_dbc()
        with dbc.cursor() as c:
            c.execute('SELECT id, name FROM users')
            actual = [d[0] for d in c.description]
            
        self.assertEqual(['id', 'name'], actual)



