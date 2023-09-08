from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.Base import Base
from models.User import User
from models.Book import Book
from models.Transaction import Transaction

DATABASE_URL = "sqlite:///library.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class LibraryCLI:

    def __init__(self):
        self.session = Session()

    def add_book(self):
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")

        new_book = Book(title=title, author=author, isbn=isbn)
        self.session.add(new_book)
        self.session.commit()
        print(f"Book {title} added successfully!")

    def register_user(self):
        user_name = input("Enter your username: ")
        email = input("Enter your email: ")

        existing_user = self.session.query(User).filter_by(username=user_name).first()
        if existing_user:
            print(f"Username {user_name} already exists!")
            return

        new_user = User(username=user_name, email=email)
        self.session.add(new_user)
        self.session.commit()
        print(f"User {user_name} registered successfully!")

    def delete_user(self):
        username = input("Enter the username to delete: ")
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            print(f"User {username} deleted successfully!")
        else:
            print("User not found!")

    def delete_book(self):
        isbn = input("Enter the ISBN of the book to delete: ")
        book = self.session.query(Book).filter_by(isbn=isbn).first()
        if book:
            self.session.delete(book)
            self.session.commit()
            print(f"Book with ISBN {isbn} deleted successfully!")
        else:
            print("Book not found!")

    def checkout_book(self):
        user_name = input("Enter your username: ")
        user = self.session.query(User).filter_by(username=user_name).first()

        if not user:
            print("User not found! Please register.")
            return

        isbn = input("Enter the ISBN of the book you want to checkout: ")
        book = self.session.query(Book).filter_by(isbn=isbn, is_available=True).first()

        if not book:
            print("Book not available for checkout!")
            return

        book.is_available = False
        transaction = Transaction(user=user, book=book)
        self.session.add(transaction)
        self.session.commit()
        print(f"Book {book.title} has been checked out!")

    def return_book(self):
        user_name = input("Enter your username: ")
        user = self.session.query(User).filter_by(username=user_name).first()

        if not user:
            print("User not found!")
            return

        isbn = input("Enter the ISBN of the book you want to return: ")
        book = self.session.query(Book).filter_by(isbn=isbn, is_available=False).first()

        if not book:
            print("Book not found or it's not checked out!")
            return

        transaction = self.session.query(Transaction).filter_by(user=user, book=book).first()
        if transaction:
            book.is_available = True
            self.session.delete(transaction)
            self.session.commit()
            print(f"Book {book.title} has been returned!")

    def search_book(self):
        keyword = input("Enter keyword (title/author/ISBN): ")
        matched_books = self.session.query(Book).filter(
            Book.title.contains(keyword) | 
            Book.author.contains(keyword) | 
            Book.isbn.contains(keyword)
        ).all()

        if not matched_books:
            print("No books found!")
            return

        for book in matched_books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available: {book.is_available}")

    def view_all_users(self):
        users = self.session.query(User).all()
        for user in users:
            print(f"Username: {user.username}, Email: {user.email}")

    def view_all_books(self):
        books = self.session.query(Book).all()
        for book in books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available: {book.is_available}")

    def run(self):
        while True:
            print("\nLibraryCLI Menu:")
            print("1. Register User")
            print("2. Add Book")
            print("3. Search Book")
            print("4. Checkout Book")
            print("5. Return Book")
            print("6. Delete User")
            print("7. Delete Book")
            print("8. View All Users")
            print("9. View All Books")
            print("10. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.search_book()
            elif choice == "4":
                self.checkout_book()
            elif choice == "5":
                self.return_book()
            elif choice == "6":
                self.delete_user()
            elif choice == "7":
                self.delete_book()
            elif choice == "8":
                self.view_all_users()
            elif choice == "9":
                self.view_all_books()
            elif choice == "10":
                print("Thank you for using LibraryCLI!")
                break
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    cli = LibraryCLI()
    cli.run()

    
