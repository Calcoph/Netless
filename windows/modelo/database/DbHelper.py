import sqlite3
from __future__ import annotations
from contracts import ChatContract, EnviableContract, EnviablesChatContract, FicheroContract, MensajeContract, OpcionesContract, UsuarioContract, WhiteListContract, Contract

from ..configuración import OpcionesUsuario


DBType = str | int
DBParameters = tuple[DBType] | dict[str, DBType]

class SelectResult:
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cur = cursor

    def fetch_one(self) -> DBType:
        self.cur.fetchone()
    
    def fetch_many(self, amount) -> list[DBType]:
        self.cur.fetchmany(amount)
    
    def fetch_all(self) -> list[DBType]:
        self.cur.fetchall()

class DbHelper:
    DB_NAME: str = "NetLess.db"
    CONTRACTS: list[Contract] = [
        ChatContract,
        EnviableContract,
        EnviablesChatContract,
        FicheroContract,
        MensajeContract,
        OpcionesContract,
        UsuarioContract,
        WhiteListContract
    ]

    DB: DbHelper = None

    def __init__(self) -> None:
        """NUNCA LLAMAR A LA CONSTRUCTORA DIRECTAMENTE, usar .get()"""

        if self.DB is None:
            self._init_db()
            self.DB = self
        else:
            raise SystemError
    
    def _init_db(self) -> None:
        """NUNCA LLAMAR A ESTA FUNCIÓN, usar .get()"""
        self.con = sqlite3.connect(self.DB_NAME)
        self.cur = self.con.cursor()
        tablas_creadas = self.cur.execute("SELECT name FROM sqlite_master").fetchall()
        for contract in self.CONTRACTS:
            if contract.TABLE_NAME not in tablas_creadas:
                self.cur.execute(contract.SQL_CREATE_ENTRIES)
        
        if len(self.cur.execute(f"SELECT * FROM {OpcionesContract.TABLE_NAME}").fetchall()) == 0:
            # No hay opciones
            # Hay que inicializar la tabla
            id = OpcionesUsuario.generar_id_aleatorio()
            alias_por_defecto = "(Sin alias)"
            self.cur.execute(f"INSERT INTO {OpcionesContract.TABLE_NAME}({OpcionesContract.COLUMN_NAME_ID}, {OpcionesContract.COLUMN_NAME_ALIAS}) VALUES ({id}, {alias_por_defecto})");

        self.con.commit()

    
    def get() -> DbHelper:
        if DbHelper.DB is None:
            DbHelper()
        
        return DbHelper.DB

    def insert(self, table_name: str, value: tuple[DBType], column_names: list[str]=[]) -> int:
        if len(column_names) == 0:
            column_names_str = ""
        else:
            column_names_str = "("
            for column_name in column_names:
                column_names_str += column_name
                column_names_str += ","
            column_names_str = column_names_str[:-1] # Remove last ","
            column_names_str += ")"
        sql_string = f"INSERT INTO {table_name}{column_names_str} VALUES ?"

        self.cur.execute(sql_string, value)
        return self.cur.lastrowid
    
    def select(self, table_name: str, column_names: list[str]=["*"], where: str="", where_values: DBParameters=None) -> SelectResult:
        if len(column_names) == 1:
            column_names_str = column_names[0]
        else:
            column_names_str = "("
            for column_name in column_names:
                column_names_str += column_name
                column_names_str += ","
            column_names_str = column_names_str[:-1] # Remove last \n
            column_names_str += ")"
        sql_str = f"SELECT {column_names_str} FROM {table_name}"
        if where != "":
            sql_str += f"WHERE {where}"
        
        return SelectResult(self.cur.execute(sql_str, where_values))

    def join_select(
        self,
        table1_name: str,
        table2_name: str,
        table1_join_column: str,
        table2_join_column: str,
        column_names: list[str]=["*"],
        where: str="",
        where_values: DBParameters=None
    ) -> SelectResult:
        if len(column_names) == 1:
            column_names_str = column_names[0]
        else:
            column_names_str = "("
            for column_name in column_names:
                column_names_str += column_name
                column_names_str += ","
            column_names_str = column_names_str[:-1] # Remove last \n
            column_names_str += ")"
        sql_str = f"SELECT {column_names_str} FROM {table1_name}"
        sql_str += f"INNER JOIN {table2_name} ON {table1_name}.{table1_join_column} = {table2_name}.{table2_join_column}"
        if where != "":
            sql_str += f"WHERE {where}"
        
        return SelectResult(self.cur.execute(sql_str, where_values))

    def delete(self, table_name: str, where: str, where_values: DBParameters):
        sql_str = f"DELETE FROM {table_name} WHERE {where}"

        self.cur.execute(sql_str, where_values)
