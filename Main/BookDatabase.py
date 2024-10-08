import sqlite3
from typing import Any

class BookDatabase:
    # /////////////////////////////////////////////
    # Constructor & Destructor
    # /////////////////////////////////////////////
    def __init__(self, databasePath: str) -> None:
        self.connection: sqlite3.Connection = sqlite3.connect(databasePath)

        self.SetupDatabase()

    def __del__(self) -> None:
        self.connection.close()

    def SetupDatabase(self) -> None:
        c: sqlite3.Cursor = self.connection.cursor()

        # Create Authors Table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS Authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create Books Table if it doesn't exist
        c.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            genre TEXT,
            price REAL,
            quantity INTEGER,
            FOREIGN KEY (author_id) REFERENCES Authors (author_id)
        )
        ''')

        self.Commit()

    # /////////////////////////////////////////////
    # Raw SQL commands
    # /////////////////////////////////////////////
    # Executes raw SQLite command
    def Execute(self, command: str, params: tuple[Any] = (), commit: bool = False) -> None:
        c: sqlite3.Cursor = self.connection.cursor()
        try:
            c.execute(command, params)
            if commit:
                self.Commit()
        finally:
            c.close()

    # Commits the previous executed commands
    def Commit(self) -> None:
        self.connection.commit()

    # Clears the data from database (keeps structure)
    def ClearData(self) -> None:
        c: sqlite3.Cursor = self.connection.cursor()
        try:
            # Delete all records from Books and Authors tables
            c.execute("DELETE FROM Books")
            c.execute("DELETE FROM Authors")
            self.Commit()
        finally:
            c.close()

    # Clears everything from database (data & structure)
    def ClearAll(self) -> None:
        c: sqlite3.Cursor = self.connection.cursor()
        try:
            # Drop the tables
            c.execute("DROP TABLE IF EXISTS Books")
            c.execute("DROP TABLE IF EXISTS Authors")
            self.Commit()
        finally:
            c.close()

    # /////////////////////////////////////////////
    # Custom SQL commands
    # /////////////////////////////////////////////
    def AddBook(self, title: str, author: str, genre: str, price: float, quantity: int) -> None:
        c: sqlite3.Cursor = self.connection.cursor()
    
        try:
            # Check if author exists
            c.execute("SELECT author_id FROM Authors WHERE name=?", (author,))
            sqlAuthor = c.fetchone()
            
            # Get author ID (new or old (if exists))
            authorID: int = 0
            if sqlAuthor is None:
                c.execute("INSERT INTO Authors (name) VALUES (?)", (author,))
                authorID = c.lastrowid
            else:
                authorID = sqlAuthor[0]
            
            # Insert new book
            c.execute("INSERT INTO Books (title, author_id, genre, price, quantity) VALUES (?, ?, ?, ?, ?)", (title, authorID, genre, price, quantity))

            # Send the command queue (actually executes command)
            self.Commit()
        finally:
            c.close()

    def GetBooks(self) -> list[Any]:
        c: sqlite3.Cursor = self.connection.cursor()

        try:
            c.execute('''
                SELECT Books.title, Authors.name, Books.genre, Books.price, Books.quantity
                FROM Books
                JOIN Authors ON Books.author_id = Authors.author_id
            ''')

            # Return command result
            return c.fetchall()
        finally:
            c.close()