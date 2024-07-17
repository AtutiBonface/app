import sqlite3
def initiate_database():
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS downloads 
                ( id INTEGER PRIMARY KEY, filename TEXT,address TEXT, filesize TEXT,downloaded TEXT, status TEXT, modification_date TEXT, path TEXT )''')
    conn.commit()
    conn.close()

def add_data(filename, address,filesize, downloaded, status, modification_date, path):
    conn2 = sqlite3.connect('downloads.db')
    cursor = conn2.cursor()

    cursor.execute(''' INSERT INTO downloads 
                   (filename, address,filesize, downloaded,status, modification_date, path) VALUES(?,?,?,?,?, ?, ?) ''', 
                   (filename, address, filesize, downloaded, status, modification_date, path))
    conn2.commit()
    conn2.close()

def get_all_data():
    conn3 = sqlite3.connect('downloads.db')
    cursor = conn3.cursor()
    cursor.execute('''SELECT * FROM downloads''')

    my_list = cursor.fetchall()    

    conn3.close()
    print(my_list)
    if len(my_list) == 0:
        print("there is no data now !")

def get_incomplete_downloads():
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()
    cursor.execute(''' SELECT * FROM downloads WHERE status != "complete"''')
    failed = cursor.fetchall()

    print(failed)
    if len(failed) == 0:
        print('No incomplete files')

def get_complete_downloads():
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM downloads WHERE status == "complete" ''')
    complete_downloads = cursor.fetchall()
    print(complete_downloads)
    if len(complete_downloads) == 0:
        print('No complete files ')

def update_data(filename1, filename2):
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()
    cursor.execute(''' UPDATE downloads SET filename = ?  WHERE filename = ? ''', (filename1, filename2))
    conn.commit()
    conn.close()
def delete_all_data():
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM downloads''')
    
    conn.commit()
    conn.close()

def delete_individual_file(filename):
    conn = sqlite3.connect('downloads.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM downloads WHERE  filename = ?''', (filename,))
    conn.commit()
    conn.close()

initiate_database()
#update_data('music.cdsj', 'rihanna-work-ft-drake.mp4')

#delete_all_data()
#delete_individual_file('rihanna-work-ft-drake.mp4')
print('--------------------------------- complete------------------------------')
get_complete_downloads()
print('---------------------------------incomplete------------------------------')
get_incomplete_downloads()
print('---------------------------------all------------------------------')
get_all_data()
