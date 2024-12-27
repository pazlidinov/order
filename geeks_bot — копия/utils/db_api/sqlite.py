import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
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

    def create_table_customers(self):
        sql = """
        CREATE TABLE Customers (
            id int NOT NULL,
            name varchar(255) NOT NULL,
            surname varchar(255) NOT NULL,
            username varchar(255) NOT NULL,            
            phone varchar(255) NOT NULL,           
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def add_customer(
        self,
        id: int,
        name: str,
        surname: str,
        username: str,
        phone: str,
    ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, name, surname, username, phone) VALUES(1, 'John', 'Smith', 'jsmith', '+1234567890')"

        sql = """
        INSERT INTO Customers(id, name, surname, username, phone) VALUES(?, ?, ?, ?,?)
        """
        self.execute(
            sql,
            parameters=(id, name, surname, username, phone),
            commit=True,
        )

    def select_all_customers(self):
        sql = """
        SELECT * FROM Customers
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Customers WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_customers(self):
        return self.execute("SELECT COUNT(*) FROM Customers;", fetchone=True)

    def delete_customers(self):
        self.execute("DELETE FROM Customers WHERE TRUE", commit=True)


def logger(statement):
    print(
        f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
    )
