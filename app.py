"""
Library Management System - Web Version
Flask-based web application with JSON persistence
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# ======================== BOOK CLASS ========================
class Book:
    def __init__(self, book_id: str, title: str, author: str, quantity: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity
    
    def to_dict(self) -> Dict:
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'quantity': self.quantity
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Book':
        return Book(
            data['book_id'],
            data['title'],
            data['author'],
            data['quantity']
        )

# ======================== MEMBER CLASS ========================
class Member:
    def __init__(self, member_id: str, name: str, issued_books: Optional[List[str]] = None):
        self.member_id = member_id
        self.name = name
        self.issued_books = issued_books if issued_books else []
    
    def to_dict(self) -> Dict:
        return {
            'member_id': self.member_id,
            'name': self.name,
            'issued_books': self.issued_books
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Member':
        return Member(
            data['member_id'],
            data['name'],
            data.get('issued_books', [])
        )

# ======================== TRANSACTION CLASS ========================
class Transaction:
    def __init__(self, member_id: str, book_id: str, action: str, timestamp: Optional[str] = None):
        self.member_id = member_id
        self.book_id = book_id
        self.action = action
        self.timestamp = timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            'member_id': self.member_id,
            'book_id': self.book_id,
            'action': self.action,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Transaction':
        return Transaction(
            data['member_id'],
            data['book_id'],
            data['action'],
            data.get('timestamp')
        )

# ======================== LIBRARY CLASS ========================
class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.transactions: List[Transaction] = []
        
        self.books_file = 'books.json'
        self.members_file = 'members.json'
        self.transactions_file = 'transactions.json'
        
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.books_file):
                with open(self.books_file, 'r') as f:
                    books_data = json.load(f)
                    self.books = {book_id: Book.from_dict(data) 
                                 for book_id, data in books_data.items()}
            
            if os.path.exists(self.members_file):
                with open(self.members_file, 'r') as f:
                    members_data = json.load(f)
                    self.members = {member_id: Member.from_dict(data) 
                                   for member_id, data in members_data.items()}
            
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    transactions_data = json.load(f)
                    self.transactions = [Transaction.from_dict(data) 
                                        for data in transactions_data]
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        try:
            with open(self.books_file, 'w') as f:
                books_data = {book_id: book.to_dict() 
                             for book_id, book in self.books.items()}
                json.dump(books_data, f, indent=4)
            
            with open(self.members_file, 'w') as f:
                members_data = {member_id: member.to_dict() 
                               for member_id, member in self.members.items()}
                json.dump(members_data, f, indent=4)
            
            with open(self.transactions_file, 'w') as f:
                transactions_data = [transaction.to_dict() 
                                    for transaction in self.transactions]
                json.dump(transactions_data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_book(self, book_id: str, title: str, author: str, quantity: int) -> tuple:
        if book_id in self.books:
            return False, f"Book with ID '{book_id}' already exists!"
        
        if quantity < 0:
            return False, "Quantity cannot be negative!"
        
        new_book = Book(book_id, title, author, quantity)
        self.books[book_id] = new_book
        self.save_data()
        return True, f"Book '{title}' added successfully!"
    
    def search_book(self, search_term: str) -> List[Book]:
        search_term = search_term.lower()
        results = []
        
        for book in self.books.values():
            if (search_term in book.book_id.lower() or 
                search_term in book.title.lower()):
                results.append(book)
        
        return results
    
    def remove_book(self, book_id: str) -> tuple:
        if book_id not in self.books:
            return False, f"Book with ID '{book_id}' not found!"
        
        book = self.books[book_id]
        
        for member in self.members.values():
            if book_id in member.issued_books:
                return False, f"Cannot remove book! It is currently issued to member '{member.name}'."
        
        del self.books[book_id]
        self.save_data()
        return True, f"Book '{book.title}' removed successfully!"
    
    def register_member(self, member_id: str, name: str) -> tuple:
        if member_id in self.members:
            return False, f"Member with ID '{member_id}' already exists!"
        
        new_member = Member(member_id, name)
        self.members[member_id] = new_member
        self.save_data()
        return True, f"Member '{name}' registered successfully!"
    
    def issue_book(self, member_id: str, book_id: str) -> tuple:
        if member_id not in self.members:
            return False, f"Member with ID '{member_id}' not found!"
        
        if book_id not in self.books:
            return False, f"Book with ID '{book_id}' not found!"
        
        member = self.members[member_id]
        book = self.books[book_id]
        
        if book_id in member.issued_books:
            return False, f"Book '{book.title}' is already issued to {member.name}!"
        
        if book.quantity <= 0:
            return False, f"Book '{book.title}' is currently not available!"
        
        book.quantity -= 1
        member.issued_books.append(book_id)
        
        transaction = Transaction(member_id, book_id, 'issue')
        self.transactions.append(transaction)
        
        self.save_data()
        return True, f"Book '{book.title}' issued to {member.name} successfully!"
    
    def return_book(self, member_id: str, book_id: str) -> tuple:
        if member_id not in self.members:
            return False, f"Member with ID '{member_id}' not found!"
        
        if book_id not in self.books:
            return False, f"Book with ID '{book_id}' not found!"
        
        member = self.members[member_id]
        book = self.books[book_id]
        
        if book_id not in member.issued_books:
            return False, f"Book '{book.title}' is not issued to {member.name}!"
        
        book.quantity += 1
        member.issued_books.remove(book_id)
        
        transaction = Transaction(member_id, book_id, 'return')
        self.transactions.append(transaction)
        
        self.save_data()
        return True, f"Book '{book.title}' returned by {member.name} successfully!"

# Initialize library
library = Library()

# ======================== ROUTES ========================

@app.route('/')
def index():
    return render_template('index.html', 
                         books_count=len(library.books),
                         members_count=len(library.members),
                         transactions_count=len(library.transactions))

@app.route('/books')
def books():
    return render_template('books.html', books=library.books.values())

@app.route('/members')
def members():
    return render_template('members.html', members=library.members.values(), books=library.books)

@app.route('/transactions')
def transactions():
    return render_template('transactions.html', 
                         transactions=library.transactions,
                         books=library.books,
                         members=library.members)

# API Routes
@app.route('/api/books/add', methods=['POST'])
def api_add_book():
    data = request.json
    success, message = library.add_book(
        data['book_id'],
        data['title'],
        data['author'],
        int(data['quantity'])
    )
    return jsonify({'success': success, 'message': message})

@app.route('/api/books/search', methods=['GET'])
def api_search_book():
    search_term = request.args.get('q', '')
    results = library.search_book(search_term)
    return jsonify({'books': [book.to_dict() for book in results]})

@app.route('/api/books/remove', methods=['POST'])
def api_remove_book():
    data = request.json
    success, message = library.remove_book(data['book_id'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/members/register', methods=['POST'])
def api_register_member():
    data = request.json
    success, message = library.register_member(data['member_id'], data['name'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/books/issue', methods=['POST'])
def api_issue_book():
    data = request.json
    success, message = library.issue_book(data['member_id'], data['book_id'])
    return jsonify({'success': success, 'message': message})

@app.route('/api/books/return', methods=['POST'])
def api_return_book():
    data = request.json
    success, message = library.return_book(data['member_id'], data['book_id'])
    return jsonify({'success': success, 'message': message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
