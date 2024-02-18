import sqlite3
import os
import json
from shutil import copyfile
import time

def extract_cookies(domain=None, start_date=None, end_date=None, cookie_name=None, output_file='cookies.json'):
    # Find the directory where Chrome cookies are stored
    user_data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default'
    temp_db_path = user_data_path + r'\Cookies_temp'

    # Copy the Cookies file
    copyfile(user_data_path + r'\Cookies', temp_db_path)

    # Create an SQLite connection
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    # Construct the SQL query based on domain, date range, and cookie name
    query = 'SELECT * FROM cookies WHERE 1=1'
    if domain:
        query += f" AND host_key LIKE '%{domain}%'"
    if start_date:
        query += f" AND creation_utc >= {start_date}"
    if end_date:
        query += f" AND creation_utc <= {end_date}"
    if cookie_name:
        query += f" AND name = '{cookie_name}'"

    # Select and serialize the cookies
    cursor.execute(query)
    cookies = cursor.fetchall()
    cookies_json = json.dumps(cookies, indent=4)
    print(cookies_json)

    # Close the connection
    conn.close()

    # Remove the temporary database
    os.remove(temp_db_path)

    # Save the cookies to a JSON file
    with open(output_file, 'w') as file:
        file.write(cookies_json)

    # Return the extracted cookies
    return cookies

def edit_cookie(cookie_name, new_value):
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE cookies SET value = '{new_value}' WHERE name = '{cookie_name}'")
    conn.commit()
    conn.close()

def delete_cookie(cookie_name):
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM cookies WHERE name = '{cookie_name}'")
    conn.commit()
    conn.close()

def remove_expired_cookies():
    current_time = int(time.time() * 1000000)  # Convert current time to microseconds
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM cookies WHERE expires_utc != 0 AND expires_utc <= {current_time}")
    conn.commit()
    conn.close()

# Example usage
extracted_cookies = extract_cookies(domain='example.com', start_date=1646713200000, end_date=1646716800000, cookie_name='session', output_file='cookies.json')