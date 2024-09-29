import sys
import random
from typing import Any

from BookDatabase import BookDatabase

def main(argv: list[str]):
    books: BookDatabase = BookDatabase("Main/assets/books.db")

    books.AddBook("Mysterious Death", "Mystery Author", "Thriller", 19.99, random.randint(1, 10000))

    books: list[Any] = books.GetBooks()
    for book in books:
        print(f"Book found: {book}")

if __name__ == '__main__':
    main(sys.argv)