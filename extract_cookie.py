import sqlite3
import os
from shutil import copyfile

# Find the directory where Chrome cookies are stored
user_data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default'
temp_db_path = user_data_path + r'\Cookies_temp'

# Copy the Cookies file
copyfile(user_data_path + r'\Cookies', temp_db_path)

# Create an SQLite connection
conn = sqlite3.connect(temp_db_path)
cursor = conn.cursor()

# Select and print the cookies
cursor.execute('SELECT * FROM cookies')
cookies = cursor.fetchall()
for cookie in cookies:
    print(cookie)

# Close the connection
conn.close()

# Remove the temporary database
os.remove(temp_db_path)