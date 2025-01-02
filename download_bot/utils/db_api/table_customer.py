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
        id: int,
        username: str,
        name: str,
        last_name: str,
        offer_link: str,
        invited: int,
        balance: int,
    ):
        # SQL_EXAMPLE = "INSERT INTO Users(id,  username, name, last_name, offer_link) VALUES(1, 'John', 'Smith', 'jsmith', 'htpps://t.me/id')"

        sql = """
        INSERT INTO main_app_customer(id,  username, name, last_name, offer_link,invited, balance) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            sql,
            parameters=(id, username, name, last_name, offer_link, invited, balance),
            commit=True,
        )

    def select_customer(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Customer where id=1 AND Name='John'"
        sql = "SELECT * FROM main_app_customer WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_customer(self, id: int, invited: int, balance: int):
        # SQL_EXAMPLE = "UPDATE customer SET invited=5 AND balance=50 WHERE id=5"

        sql = f"""
        UPDATE main_app_customer SET invited = invited + ?, balance = balance + ? WHERE id = ?
        """
        return self.execute(sql, parameters=(invited, balance, id), commit=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )
