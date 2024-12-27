import sqlite3


class DatabaseRegistration:
    def __init__(self, path_to_db="training_center/db.sqlite3"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
        self,
        sql: str,
        parameters: tuple = None,
        fetchone=False,
        fetchall=False,
        commit=False,
    ):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters,)
        connection.execute("PRAGMA foreign_keys = 1")

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def add_registration(
        self,
        # id: int,
        customer: int,
        course: int,
        date: str,
    ):
        # SQL_EXAMPLE = "INSERT INTO main_registration(customer, course, date) VALUES(1, 'John', 'Smith', 'jsmith', '+1234567890')"

        sql = """
        INSERT INTO main_registration(customer, course, date) VALUES(?, ?, ?)
        """
        self.execute(
            sql,
            parameters=(customer, course, date),
            commit=True,
        )

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM main_registration where id=1 AND Name='John'"
        sql = "SELECT * FROM main_registration WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )
