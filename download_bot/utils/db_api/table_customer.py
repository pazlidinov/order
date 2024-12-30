import sqlite3


class DatabaseCustomer:
    def __init__(self, path_to_db="web/db.sqlite3"):
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
        cursor.execute(sql, parameters)

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

    def add_customer(
        self,
        telegram_id: int,
        username: str,
        name: str,
        last_name: str,
        offer_link: str,
    ):
        # SQL_EXAMPLE = "INSERT INTO Users(telegram_id,  username, name, last_name, offer_link) VALUES(1, 'John', 'Smith', 'jsmith', 'htpps://t.me/telegram_id')"

        sql = """
        INSERT INTO main_app_customer(telegram_id,  username, name, last_name, offer_link) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(
            sql,
            parameters=(telegram_id, username, name, last_name, offer_link),
            commit=True,
        )

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM main_customer WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_user(self, invited, balance):
        # SQL_EXAMPLE = "UPDATE Users SET invited=5 WHERE balance=50"

        sql = f"""
        UPDATE Users SET invited=? WHERE balance=?
        """
        return self.execute(sql, parameters=(invited, balance), commit=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )
