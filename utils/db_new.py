import sqlite3
import pymysql.cursors   

class Database:
    def __init__(self, db_file):
        # self.connection = sqlite3.connect(db_file)
        self.connection = pymysql.connect(host='127.0.0.1',
                             user='Flashlight',
                             password='qwert123',                             
                             db='telegram_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor) 
        print ("connect successful!!") 

        self.cursor = self.connection.cursor()

    def create_tables(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS subscribers (
                    id INT PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    country TEXT,
                    city TEXT,
                    geonameid INT,
                    latitude TEXT,
                    longitude TEXT
                    ) """)    
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS youtube_video (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    type TEXT,
                    date TEXT
                    ) """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS admins (
                    id INT PRIMARY KEY,
                    role TEXT,
                    memo TEXT
                    ) """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS feedback (
                    id INT PRIMARY KEY,
                    review TEXT
                     ) """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS active_sub (
                    id INT PRIMARY KEY,
                    active TEXT,
                    allow_spam TEXT
                    ) """)

            self.cursor.execute("""CREATE TABLE IF NOT EXISTS stats (
                    id_user INT,
                    command TEXT,
                    date TEXT
                    ) """)

            self.connection.commit()
            
    def stats(self, id_user, command, date):
        with self.connection:
            self.cursor.execute("INSERT INTO stats  VALUES (?,?,?)", (id_user, command, date, ))
            self.connection.commit()

    def add_to_active_sub_table(self, id_user, active, allow_spam):
        with self.connection:
            self.cursor.execute("INSERT INTO active_sub  VALUES (?,?,?)", (id_user, active, allow_spam, ))
            self.connection.commit()        

    def update_sub(self, id_user, active, allow_spam):
        with self.connection:
            self.cursor.execute("UPDATE active_sub SET active = (?), allow_spam = (?) WHERE id = (?)", (active,allow_spam, id_user, ))
            self.connection.commit()        

    def sub_spam_allow(self,spam_allow):
        with self.connection: 
            result = self.cursor.execute("SELECT id FROM active_sub WHERE allow_spam = (?)", (spam_allow,)).fetchall()
            return(result) 

    def subscribers_to_db(self, id,first_name,username, country=None, city=None, geonameid=None, latitude=None, longitude=None):
        with self.connection:
            self.cursor.execute("INSERT OR REPLACE INTO subscribers VALUES (?, ?, ?, ?, ?, ?, ?, ?) ", \
                (id, first_name, username,country,city,geonameid,latitude,longitude,))
            self.connection.commit()

    def subscribers_search_by_id(self,id):
        with self.connection: 
            result = self.cursor.execute("SELECT id FROM subscribers WHERE id = (?)", (id,)).fetchall()
            return(result) 

    def show_all_from_table(self, table):
        with self.connection:    
            result = self.cursor.execute("SELECT * FROM "+table+"").fetchall()
            return(result)

    def feedback_to_db(self, id, review):
        with self.connection:
            self.cursor.execute("INSERT OR REPLACE INTO feedback VALUES (?,?)", (id, review, ))
            self.connection.commit()

    def youtube_video_to_db(self, url, title, type, data):
        with self.connection:
            self.cursor.execute("INSERT OR REPLACE INTO youtube_video VALUES (?,?,?,?)", (url, title, type, data, ))
            self.connection.commit()

    def youtube_video_show_all(self, type,num):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM youtube_video WHERE type = (?) ORDER BY date DESC", (type,)).fetchmany(num)
            return (result)

    def youtube_video_search_url(self, url):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM youtube_video WHERE url = (?) ", (url,)).fetchall()
            return(result)

    def check_location(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM subscribers WHERE id = (?) AND geonameid != (?) ", (id,'None',)).fetchone()
            return(result)

    def admins_to_db(self, id, role, memo):
        with self.connection:
            self.cursor.execute("INSERT OR REPLACE INTO admins VALUES (?, ?, ?)", (id, role, memo, ))
            self.connection.commit()

    def adm_del_from_db(self, id):
        with self.connection:
            self.cursor.execute('DELETE FROM admins WHERE id = (?)', (id,))
            self.connection.commit()
                    
    def drop_table(self):
        with self.connection:
            self.cursor.execute('DROP TABLE stats')
            self.connection.commit()

# db = Database('data/bot.db')    
#
db = Database()   
            