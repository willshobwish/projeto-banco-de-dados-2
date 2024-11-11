# app/database_setup.py
import mysql.connector
from datetime import datetime

# Establish connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",
    database="mydb"
)

cursor = db.cursor()

# Create `users` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
);
""")

# Create `images` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(300) NOT NULL,
    is_processed BOOLEAN DEFAULT FALSE NOT NULL,
    owner_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

# Create `processed_images` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS processed_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(300) NOT NULL,
    original_image_id INT NOT NULL,
    description VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (original_image_id) REFERENCES images(id) ON DELETE CASCADE
);
""")

# Commit and close connection
db.commit()
cursor.close()
db.close()
