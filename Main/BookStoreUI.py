import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem, QAction)
from BookDatabase import BookDatabase

class BookStoreUI(QMainWindow):
    # /////////////////////////////////////////////
    # Constructor & Destructor
    # /////////////////////////////////////////////
    def __init__(self, db: BookDatabase):
        super().__init__()

        self.database: BookDatabase = db

        # Configure the UI window
        self.setWindowTitle("Modern Bookstore Inventory")
        self.setGeometry(100, 100, 600, 400)

        # Initialize the central widget and layout
        self.centerWidget: QWidget = QWidget(self)
        self.setCentralWidget(self.centerWidget)
        self.mainLayout: QVBoxLayout = QVBoxLayout(self.centerWidget)

        # Keep a reference to the "View Books" window, so it doesnt
        # close on opening.
        self.booksWindow: QWidget | None = None

        # Initialize QT elements
        self.InitUI()
        self.InitMenubar()

    def InitUI(self):
        # Title input
        self.titleLabel = QLabel('Title:')
        self.titleEntry = QLineEdit()
        self.titleEntry.setPlaceholderText('Enter book title')

        # Author input
        self.authorLabel = QLabel('Author:')
        self.authorEntry = QLineEdit()
        self.authorEntry.setPlaceholderText('Enter author name')

        # Genre input
        self.genreLabel = QLabel('Genre:')
        self.genreEntry = QLineEdit()
        self.genreEntry.setPlaceholderText('Enter genre')

        # Price input
        self.priceLabel = QLabel('Price:')
        self.priceEntry = QLineEdit()
        self.priceEntry.setPlaceholderText('Enter price (numeric)')

        # Quantity input
        self.quantityLabel = QLabel('Quantity:')
        self.quantityEntry = QLineEdit()
        self.quantityEntry.setPlaceholderText('Enter quantity (numeric)')

        # Add Book button
        self.addBookButton = QPushButton("Add Book")
        self.addBookButton.clicked.connect(self.AddBook)

        # Clear Table button
        self.clearTableButton = QPushButton("Clear Table")
        self.clearTableButton.clicked.connect(self.ClearTable)

        # Style the UI elements
        self.SetStyles()

        # Add widgets to the layout
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.titleEntry)
        self.mainLayout.addWidget(self.authorLabel)
        self.mainLayout.addWidget(self.authorEntry)
        self.mainLayout.addWidget(self.genreLabel)
        self.mainLayout.addWidget(self.genreEntry)
        self.mainLayout.addWidget(self.priceLabel)
        self.mainLayout.addWidget(self.priceEntry)
        self.mainLayout.addWidget(self.quantityLabel)
        self.mainLayout.addWidget(self.quantityEntry)
        self.mainLayout.addWidget(self.addBookButton)
        self.mainLayout.addWidget(self.clearTableButton)

    def InitMenubar(self):
        # Create the menu bar
        menubar = self.menuBar()

        # Create 'View' menu
        viewMenu = menubar.addMenu('View')

        # Add 'View All Books' action
        viewBooksAction = QAction('View All Books', self)
        viewBooksAction.triggered.connect(self.ShowBooks)

        # Set the viewing action
        viewMenu.addAction(viewBooksAction)

    def SetStyles(self):
        # General Window Styling
        self.centerWidget.setStyleSheet("""
            QWidget {
                background-color: #282c34;
                color: #ffffff;
                font-family: Arial;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border-radius: 5px;
                border: 1px solid #61dafb;
                background-color: #3b4048;
                color: #ffffff;
            }
            QPushButton {
                font-size: 16px;
                background-color: #61dafb;
                border-radius: 10px;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #21a1f1;
            }
        """)

    def AddBook(self):
        title = self.titleEntry.text()
        author = self.authorEntry.text()
        genre = self.genreEntry.text()

        try:
            price = float(self.priceEntry.text())
            quantity = int(self.quantityEntry.text())
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Price must be a number and Quantity must be an integer.", QMessageBox.Ok)
            return

        if title and author and genre:
            self.database.AddBook(title, author, genre, price, quantity)
            QMessageBox.information(self, "Success", "Book added successfully!", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Input Error", "All fields must be filled!", QMessageBox.Ok)

    def ClearTable(self):
        # Confirm before clearing the database
        reply = QMessageBox.question(self, "Clear Database", "Are you sure you want to clear the database?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.database.ClearData()
            QMessageBox.information(self, "Success", "Database cleared!", QMessageBox.Ok)

    def ShowBooks(self):
        # Check if there's already an open books window
        if self.booksWindow is not None and self.booksWindow.isVisible():
            return

        # Create a new window for viewing books
        self.booksWindow = QWidget()
        self.booksWindow.setWindowTitle("Books in Inventory")
        self.booksWindow.setGeometry(100, 100, 600, 400)

        # Create a table to display books
        table = QTableWidget(self.booksWindow)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Title', 'Author', 'Genre', 'Price', 'Quantity'])

        # Fetch all books from the database
        books = self.database.GetBooks()

        table.setRowCount(len(books))

        # Insert data into the table
        for row, book in enumerate(books):
            for col, data in enumerate(book):
                table.setItem(row, col, QTableWidgetItem(str(data)))

        # Set table layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.booksWindow.setLayout(layout)

        self.booksWindow.show()
