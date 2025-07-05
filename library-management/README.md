# Library Management System

A simple Streamlit-based library management web app.

## Features

- Add/remove books (librarian)
- Borrow/return books (members)
- Borrowing limits by member type

## Setup

1. **Install dependencies**  
   `pip install -r requirements.txt`

2. **Run the app**  
   `streamlit run library_app.py`

3. **Run tests**  
   `pytest test_library.py`

## Project Structure

- `library_core.py`: Core logic and classes
- `library_app.py`: Streamlit UI
- `test_library.py`: Tests for core logic
- `data/`: Sample data 
