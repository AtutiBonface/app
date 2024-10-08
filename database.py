import sqlite3, os
from pathlib import Path
from app_utils import ConfigFilesHandler

path_to_data_base = Path().home() / '.blackjuice'

location = os.path.join(path_to_data_base, 'xe-blackjuice.db')

def initiate_database():   
    ConfigFilesHandler().create_config_file() 
    conn = sqlite3.connect(location)
    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS downloads 
                ( id INTEGER PRIMARY KEY, filename TEXT,address TEXT, filesize TEXT,downloaded TEXT, status TEXT, modification_date TEXT, path TEXT )''')
    conn.commit()
    conn.close()

def add_data(filename, address,filesize, downloaded, status, modification_date, path):
    conn2 = sqlite3.connect(location)
    cursor = conn2.cursor()

    cursor.execute(''' INSERT INTO downloads 
                   (filename, address,filesize, downloaded,status, modification_date, path) VALUES(?,?,?,?,?, ?, ?) ''', 
                   (filename, address, filesize, downloaded, status, modification_date, path))
    conn2.commit()
    conn2.close()

def get_all_data():
    conn3 = sqlite3.connect(location)
    cursor = conn3.cursor()
    cursor.execute('''SELECT * FROM downloads''')

    all_downloads = cursor.fetchall()    


    


    conn3.close()
    return all_downloads

def update_filename(old_name, new_name):
    old_name = os.path.basename(old_name)
    new_name = os.path.basename(new_name)

    conn = sqlite3.connect(location)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE downloads SET filename = ?  WHERE filename = ?  ''', (new_name, old_name))
    conn.commit()
    conn.close()

def get_incomplete_downloads():
    conn = sqlite3.connect(location)
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM downloads WHERE status != "completed."''')
    incomplete_downloads = cursor.fetchall()

    return incomplete_downloads

def get_complete_downloads():
    conn = sqlite3.connect(location)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM downloads WHERE status == "completed." ''')
    complete_downloads = cursor.fetchall()
    
    return complete_downloads

def update_data(filename, address,size, downloaded, status, date):
    filename = os.path.basename(filename)
    conn = sqlite3.connect(location)
    cursor = conn.cursor()
    cursor.execute(''' UPDATE downloads SET  filesize = ?, downloaded = ?, status= ?, modification_date =?  WHERE filename = ?  ''', (size, downloaded, status, date, filename))
    conn.commit()
    conn.close()
def delete_all_data():
    conn = sqlite3.connect(location)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM downloads''')
    
    conn.commit()
    conn.close()

def delete_individual_file(filename):
    conn = sqlite3.connect(location)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM downloads WHERE  filename = ?''', (filename,))

    conn.commit()
    conn.close()

def check_filename_existance(f_name):
    base_name = os.path.basename(f_name)
    conn = sqlite3.connect(location)

    cursor = conn.cursor()

    cursor.execute('''SELECT COUNT(*) FROM downloads WHERE filename = ?''', (base_name,))

    count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return count > 0



