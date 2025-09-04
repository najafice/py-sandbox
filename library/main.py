from library import Library

# Create library instance
lib = Library()

# Sample books (title, author)
sample_books = [
    ("1984", "George Orwell"),
    ("To Kill a Mockingbird", "Harper Lee"),
    ("The Great Gatsby", "F. Scott Fitzgerald"),
    ("Pride and Prejudice", "Jane Austen"),
    ("Moby-Dick", "Herman Melville"),
    ("War and Peace", "Leo Tolstoy"),
    ("The Catcher in the Rye", "J.D. Salinger"),
    ("The Hobbit", "J.R.R. Tolkien"),
    ("Crime and Punishment", "Fyodor Dostoevsky"),
    ("Brave New World", "Aldous Huxley"),
    ("The Alchemist", "Paulo Coelho"),
    ("The Picture of Dorian Gray", "Oscar Wilde"),
]

for title, author in sample_books:
    lib.add_book(title, author)

# Show the library
print(lib.show_books())

#print(lib.remove_book('The Picture of Dorian Gray'))
