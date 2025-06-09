"""OOP"""

class Book:
    def __init__(self, title, author, isbn):

        self.__title = title
        self.__author = author
        self.__isbn = isbn

    """GETTERS"""
    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_isbn(self):
        return self.__isbn

    """SETTERS"""
    def set_title(self, title):
        self.__title = title

    def set_author(self, author):
        self.__author = author

    def set_isbn(self, isbn):
        self.__isbn = isbn

    """DISPLAY"""
    def display_book_info(self):
        return f"Title: {self.__title}, Author: {self.__author}, ISBN: {self.__isbn}"


class Library:

    def __init__(self):
        self.__books = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, isbn):
        for book in self.__books:
            if book.get_isbn() == isbn:
                self.__books.remove(book)

                return f"The book of '{book.get_title()}' with ISBN '{book.get_isbn()}' has been removed successfully.\n" + "======" * 5

        return "Book not found in the library.\n" + "=====" * 5

    def list_books(self):

        if not self.__books:
            print("No books in the library.")
            print_seperator()

        else:
            for book in self.__books:
                print(book.display_book_info())
                print("------" * 5)


def main():

    library = Library()

    while True:

        print("Welcome to the Library Management System! "
              "\nWhat can i do for you?"
              ""
              "\n\n\t1. Add a Book"
              "\n\t2. Remove a Book"
              "\n\t3. List all Books"
              "\n\t4. Exit")

        pick = input("\nEnter Your choice (1-4): ").strip()
        print_seperator()

        if pick == "1":

            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            isbn = input("Enter book ISBN: ").strip()
            print (f"The '{title}' has been added successfully!")
            print_seperator()
            book = Book(title = title, author = author, isbn = isbn)
            library.add_book(book)

        elif pick == "2":

            isbn = input("Enter the ISBN of the book you want to remove: ")
            print(library.remove_book(isbn))

        elif pick == "3":

            library.list_books()

        elif pick == "4":

            print ("Thank you for using this Program, Goodbye!")
            break

        else:
            print("Invalid Choice, Enter number from 1 to 4\n")
            print_seperator()

def print_seperator():
    print ("======" * 5)

if __name__ == "__main__":
    main()