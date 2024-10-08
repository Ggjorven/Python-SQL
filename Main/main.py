import sys
from typing import Any

from PyQt5.QtWidgets import QApplication

from BookDatabase import BookDatabase
from BookStoreUI import BookStoreUI

def main(argv: list[str]):
    books: BookDatabase = BookDatabase("Main/assets/books.db")

    app = QApplication(argv)

    # Create the main window
    ui: BookStoreUI = BookStoreUI(books)
    ui.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)
