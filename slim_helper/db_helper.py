from typing import Iterable,Dict
from enum import Enum,auto

class DbType(Enum):
    SQLite = auto()
    PostgreSQL = auto()


class IDbHelper:
    """
    IDbHelper interface (support <with> statement)
    """
    
    def __init(self):
        self._db_connection=None
    
    def open(self):
        raise NotImplementedError("IDbHelper.open() is not implemented")

    def close(self):
        if self._db_connection:
            self.commit()
            self._db_connection.close()
            self._db_connection=None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def query(self, sql: str, params: Iterable = None) -> Iterable:
        cursor = self._db_connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute(self, sql: str, params: Iterable = None) -> int:
        raise NotImplementedError("IDbHelper.execute() is not implemented")

    def commit(self):
        self._db_connection.commit()

    def rollback(self):
        self._db_connection.rollback()


class DbHelper(IDbHelper):
    '''
    constructor:
        config : Database connection params
        db_type(str): Database type
    usage:
        # SQlite:
        config = {dbname:':memory:'}
        with DbHelper(config,'sqlite') as db:
            db.execute("""
            CREATE TABLE foo (
            id INTEGER PRIMARY KEY ,
            txt TEXT
            )
            """)
            db.execute("insert into foo values(?,?)",[1,'a'])
            db.execute("insert into foo values(?,?)",[2,'b'])
            db.execute("insert into foo values(?,?)",[3,'c'])
            db.commit()
            result = db.query("select * from foo where id=? and txt=?", [2, 'b'])
            print(result)
        # Or
        db=DbHelper(config,'sqlite')
        db.open()
        ...
        db.close()
        
        
        # PostgreSQL:
        config={'host':'localhost','port':'5432','dbname':'foobar','user':'foobar','password':'foobar'}
        with DbHelper(config,'postgresql') as db:
            db.execute("""
            CREATE TABLE foo (
            id INTEGER PRIMARY KEY ,
            txt TEXT
            )
            """)
            db.execute("insert into foo values(%s,%s)",[1,'a'])
            db.execute("insert into foo values(%s,%s)",[2,'b'])
            db.execute("insert into foo values(%s,%s)",[3,'c'])
            db.commit()
            result = db.query("select * from foo where id=%s and txt=%s", [2, 'b'])
            print(result)
        # Or
        db=DbHelper(config,'postgresql')
        db.open()
        ...
        db.close()
    '''

    def __init__(self, config:Dict,db_type:str):
        self._db_connection = None
        self._config=config
        self._db_map = {
            'sqlite':DbType.SQLite,
            'postgresql':DbType.PostgreSQL
        }
        if db_type not in self._db_map.keys():
            raise ValueError(f'Unknown database type: {db_type}')
        self._db_type=self._db_map[db_type]


    def open(self):
        if not self._db_connection:
            if self._db_type == DbType.SQLite:
                import sqlite3
                dbname=self._config['dbname']
                self._db_connection = sqlite3.connect(dbname)
            elif self._db_type == DbType.PostgreSQL:
                import psycopg2
                host=self._config['host']
                port=self._config['port']
                dbname=self._config['dbname']
                user=self._config['user']
                password=self._config['password']
                self._db_connection=psycopg2.connect(
                    host=host,
                    port=port,
                    dbname=dbname,
                    user=user,
                    password=password
                )
        else:
            raise RuntimeError('connection has not been closed')
            


    def execute(self, sql: str, params: Iterable = None) -> int:
        cursor = self._db_connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        if self._db_type == DbType.SQLite:
            result = self._db_connection.total_changes
        elif self._db_type == DbType.PostgreSQL:
            result = cursor.rowcount
        cursor.close()
        return result