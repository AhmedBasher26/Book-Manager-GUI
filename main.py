import tkinter as tk
from tkinter import messagebox, ttk
import csv
import requests

class Book:
    def __init__(self, title, author, genre, year, rating=None, review=None):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.rating = rating
        self.review = review

class Library:
    def __init__(self):
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]

    def search_book(self, title=None, author=None):
        if title:
            return [book for book in self.books if title.lower() in book.title.lower()]
        if author:
            return [book for book in self.books if author.lower() in book.author.lower()]

    def sort_books(self, by):
        if by == 'title':
            self.books.sort(key=lambda x: x.title)
        elif by == 'author':
            self.books.sort(key=lambda x: x.author)
        elif by == 'genre':
            self.books.sort(key=lambda x: x.genre)

    def save_to_file(self):
        with open('library.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for book in self.books:
                writer.writerow([book.title, book.author, book.genre, book.year, book.rating, book.review])

    def load_from_file(self):
        try:
            with open('library.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.books.append(Book(row[0], row[1], row[2], row[3], row[4], row[5]))
        except FileNotFoundError:
            pass

    def recommend_books(self, favorite_genre):
        return [book for book in self.books if book.genre == favorite_genre]

    def fetch_book_details(self, title):
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['items']:
                info = data['items'][0]['volumeInfo']
                return info['title'], info['authors'][0], info.get('categories', ['Unknown'])[0], info.get('publishedDate', 'Unknown')
        return None

library = Library()

def add_book_gui():
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    year = entry_year.get()
    rating = entry_rating.get()
    review = entry_review.get()
    book = Book(title, author, genre, year, rating, review)
    library.add_book(book)
    library.save_to_file()
    display_books()
    clear_entries()

def remove_book_gui():
    title = entry_title.get()
    library.remove_book(title)
    library.save_to_file()
    display_books()

def search_books_gui():
    title = entry_title.get()
    books = library.search_book(title=title)
    display_search_results(books)

def sort_books_gui(by):
    library.sort_books(by)
    display_books()

def recommend_books_gui():
    genre = entry_genre.get()
    books = library.recommend_books(genre)
    display_search_results(books)

def fetch_book_details_gui():
    title = entry_title.get()
    details = library.fetch_book_details(title)
    if details:
        entry_title.delete(0, tk.END)
        entry_title.insert(0, details[0])
        entry_author.delete(0, tk.END)
        entry_author.insert(0, details[1])
        entry_genre.delete(0, tk.END)
        entry_genre.insert(0, details[2])
        entry_year.delete(0, tk.END)
        entry_year.insert(0, details[3])

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)
    entry_review.delete(0, tk.END)

def display_books():
    for item in tree.get_children():
        tree.delete(item)
    for book in library.books:
        tree.insert('', tk.END, values=(book.title, book.author, book.genre, book.year, book.rating, book.review))

def display_search_results(books):
    for item in tree.get_children():
        tree.delete(item)
    for book in books:
        tree.insert('', tk.END, values=(book.title, book.author, book.genre, book.year, book.rating, book.review))

root = tk.Tk()
root.title("Personal Library Management System")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Title").grid(row=0, column=0)
tk.Label(frame, text="Author").grid(row=0, column=1)
tk.Label(frame, text="Genre").grid(row=0, column=2)
tk.Label(frame, text="Year").grid(row=0, column=3)
tk.Label(frame, text="Rating").grid(row=0, column=4)
tk.Label(frame, text="Review").grid(row=0, column=5)

entry_title = tk.Entry(frame)
entry_author = tk.Entry(frame)
entry_genre = tk.Entry(frame)
entry_year = tk.Entry(frame)
entry_rating = tk.Entry(frame)
entry_review = tk.Entry(frame)

entry_title.grid(row=1, column=0)
entry_author.grid(row=1, column=1)
entry_genre.grid(row=1, column=2)
entry_year.grid(row=1, column=3)
entry_rating.grid(row=1, column=4)
entry_review.grid(row=1, column=5)

btn_add = tk.Button(frame, text="Add Book", command=add_book_gui)
btn_add.grid(row=2, column=0)

btn_remove = tk.Button(frame, text="Remove Book", command=remove_book_gui)
btn_remove.grid(row=2, column=1)

btn_search = tk.Button(frame, text="Search Book", command=search_books_gui)
btn_search.grid(row=2, column=2)

btn_sort_title = tk.Button(frame, text="Sort by Title", command=lambda: sort_books_gui('title'))
btn_sort_title.grid(row=2, column=3)

btn_sort_author = tk.Button(frame, text="Sort by Author", command=lambda: sort_books_gui('author'))
btn_sort_author.grid(row=2, column=4)

btn_recommend = tk.Button(frame, text="Recommend", command=recommend_books_gui)
btn_recommend.grid(row=2, column=5)

btn_fetch = tk.Button(frame, text="Fetch Details", command=fetch_book_details_gui)
btn_fetch.grid(row=2, column=6)

tree = ttk.Treeview(root, columns=('Title', 'Author', 'Genre', 'Year', 'Rating', 'Review'), show='headings')
tree.heading('Title', text='Title')
tree.heading('Author', text='Author')
tree.heading('Genre', text='Genre')
tree.heading('Year', text='Year')
tree.heading('Rating', text='Rating')
tree.heading('Review', text='Review')
tree.pack()

display_books()

root.mainloop()
