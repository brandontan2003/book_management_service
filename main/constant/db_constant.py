import os

# Get the current working directory (inside the container)
current_dir = os.getcwd()

# Compute the absolute path by going up one directory
abs_path = os.path.join(current_dir, '../book.sqlite')

# Get the full absolute path
book_db = os.path.abspath(abs_path)

