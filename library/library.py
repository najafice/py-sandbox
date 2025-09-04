class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        self.books.append((title, author))

    def remove_book(self, title):
        """Remove a book by its title."""
        self.books = [book for book in self.books if book[0] != title]

    def search_book(self, title):
        """Search for a book by title and return its index if found."""
        for index, (book_title, author) in enumerate(self.books):
            if book_title.lower() == title.lower():
                return f"Book with title '{title}' found at index {index}"
        return "Book is not in the library!"

    def show_books(self):
        if not self.books:
            return "No books in the library."
        output = ["📚 Library Books:"]
        for idx, (title, author) in enumerate(self.books, start=1):
            output.append(f"{idx}. {title} — {author}")
        return "\n".join(output)