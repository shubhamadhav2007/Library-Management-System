# 📚 Library Management System - Web Application

A complete web-based Library Management System built with Flask, HTML, CSS, and JavaScript. This application allows you to manage books, members, and track all library transactions through an intuitive web interface.

## ✨ Features

- **Dashboard**: View statistics of books, members, and transactions at a glance
- **Book Management**: Add, view, search, and remove books
- **Member Management**: Register members and view their issued books
- **Issue/Return Books**: Easy book checkout and return system
- **Transaction History**: Complete audit trail of all library activities
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### Step 1: Download/Extract the Files

Make sure you have all the project files in a single directory:
```
library-management-web/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── books.html
│   ├── members.html
│   └── transactions.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── main.js
        ├── books.js
        └── members.js
```

### Step 2: Install Dependencies

Open your terminal/command prompt and navigate to the project directory:

```bash
cd path/to/library-management-web
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install Flask directly:

```bash
pip install Flask
```

### Step 3: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see output similar to:
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

### Step 4: Access the Website

Open your web browser and go to:
```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

🎉 **Congratulations!** Your Library Management System is now running!

## 📱 Using the Application

### Dashboard
- View total counts of books, members, and transactions
- Quick access to all major functions

### Managing Books
1. Click on "Books" in the navigation menu
2. Click "Add New Book" to add a book
3. Enter Book ID, Title, Author, and Quantity
4. Use the search bar to find specific books
5. Click the trash icon to remove a book

### Managing Members
1. Click on "Members" in the navigation menu
2. Click "Register New Member" to add a member
3. Enter Member ID and Name
4. View all members and their issued books

### Issuing Books
1. Go to the "Books" page
2. Click "Issue Book"
3. Enter Member ID and Book ID
4. Click "Issue Book" to complete

### Returning Books
1. Go to the "Members" page
2. Click "Return Book"
3. Enter Member ID and Book ID
4. Click "Return Book" to complete

### Viewing Transactions
- Click on "Transactions" to see the complete history
- Shows all book issues and returns with timestamps

## 💾 Data Persistence

The application automatically saves all data to JSON files:
- `books.json` - All book records
- `members.json` - All member records
- `transactions.json` - All transaction history

These files are created automatically in the same directory as `app.py`.

## 🌐 Deploying to the Internet

To make your website accessible on the internet, you have several options:

### Option 1: Using Python Anywhere (Free & Easy)

1. **Sign up** at https://www.pythonanywhere.com (free tier available)
2. **Upload your files**:
   - Click on "Files" tab
   - Upload all your project files
3. **Create a web app**:
   - Click on "Web" tab
   - Click "Add a new web app"
   - Choose "Flask" as framework
   - Set Python version to 3.8+
4. **Configure WSGI file**:
   - Edit the WSGI configuration file
   - Point it to your `app.py`
5. **Reload** your web app
6. Access at: `yourusername.pythonanywhere.com`

### Option 2: Using Heroku

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Create additional files**:

Create `Procfile`:
```
web: gunicorn app:app
```

Add to `requirements.txt`:
```
gunicorn==21.2.0
```

3. **Deploy**:
```bash
heroku login
heroku create your-app-name
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

### Option 3: Using Render (Free)

1. **Sign up** at https://render.com
2. **Create a new Web Service**
3. **Connect your GitHub repository** (upload code to GitHub first)
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. **Deploy** - Render will provide a URL

### Option 4: Local Network Access

To access from other devices on your local network:

1. Find your computer's local IP address:
   - Windows: Run `ipconfig` in command prompt
   - Mac/Linux: Run `ifconfig` or `ip addr`

2. Run the app:
```bash
python app.py
```

3. Access from other devices using:
```
http://YOUR-LOCAL-IP:5000
```
Example: `http://192.168.1.100:5000`

## 🛠️ Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Change port
```

### Module Not Found Error
Install missing modules:
```bash
pip install Flask
```

### Files Not Found
Ensure the directory structure is correct and all files are in their proper locations.

### Permission Denied
On Mac/Linux, you might need to use:
```bash
sudo python app.py
```

## 🔒 Security Notes

**Important**: This is a development server suitable for testing and local use. For production deployment:

1. Change the secret key in `app.py`:
```python
app.secret_key = 'your-very-secret-random-key-here'
```

2. Set `debug=False` for production
3. Use a production WSGI server (like Gunicorn)
4. Implement user authentication
5. Use a proper database instead of JSON files
6. Add input validation and sanitization

## 📝 Features to Add (Enhancement Ideas)

- User authentication (login/logout)
- Book categories and genres
- Due dates and late fees
- Email notifications
- Book reservations
- Member profiles with photos
- Export reports to PDF/Excel
- Advanced search filters
- Book cover images

## 🤝 Support

If you encounter any issues:
1. Check that all files are in the correct directories
2. Verify Python and Flask are installed correctly
3. Ensure the terminal/command prompt is in the project directory
4. Check that no other application is using port 5000

## 📄 License

This project is free to use for educational and personal purposes.

---

**Happy Library Managing! 📚✨**
