import sqlite3

def connect():
    db = sqlite3.connect('./data/bot.db')
    sql = db.cursor()
    return(db,sql) 

# Создание всех таблиц

def table_create():
    db,sql = connect()

    sql.execute("""CREATE TABLE IF NOT EXISTS subscribers (
        id INT PRIMARY KEY,
        first_name TEXT,
        username TEXT,
        country TEXT,
        city TEXT,
        geonameid INT,
        latitude TEXT,
        longitude TEXT
    ) """)

    sql.execute("""CREATE TABLE IF NOT EXISTS youtube_video (
        url TEXT PRIMARY KEY,
        title TEXT,
        type TEXT,
        date TEXT
    ) """)

    sql.execute("""CREATE TABLE IF NOT EXISTS admins (
        id INT PRIMARY KEY,
        role TEXT,
        memo TEXT
    ) """)

    sql.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INT PRIMARY KEY,
        review TEXT
    ) """)

    db.commit()
    db.close()
    return()




# Управление подписчиками
def subscribers(id,first_name,username, country=None, city=None, geonameid=None, latitude=None, longitude=None ):
    db,sql = connect()
    sql.execute("INSERT OR REPLACE INTO subscribers VALUES (?, ?, ?, ?, ?, ?, ?, ?) ", \
        (id, first_name, username,country,city,geonameid,latitude,longitude,))

    db.commit()
    db.close()
    return()

def subscribers_show_all():
    db,sql = connect()
    sql.execute("SELECT * FROM subscribers")
    result = sql.fetchall()
    return(result)  
    db.close()

def subscribers_id_list():
    db,sql = connect()
    sql.execute("SELECT id FROM subscribers")
    result = sql.fetchall()
    db.close()
    return(result)     

def subscribers_search_by_id(id):
    db,sql = connect()
    sql.execute("SELECT id FROM subscribers WHERE id = (?)", (id,))
    result = sql.fetchall()
    db.close()
    return(result)     

# feedback
def feedback(id, review):
    db,sql = connect()
    sql.execute("INSERT OR REPLACE INTO feedback VALUES (?,?)", (id, review, ))
    
    db.commit()
    db.close()
    return()

def feedback_show_all():
    db,sql = connect()
    sql.execute("SELECT * FROM feedback")
    result = sql.fetchall()
    return(result)  
    db.close()

# Добавление последних видео в бд
def youtube_video(url, title, type, data):
    db,sql = connect()

    sql.execute("INSERT OR REPLACE INTO youtube_video VALUES (?,?,?,?)", (url, title, type, data, ))
    
    db.commit()
    db.close()
    return()

# Выборка по видео на канале
def youtube_video_show_all(type,num):
    db,sql = connect()
    sql.execute("SELECT * FROM youtube_video WHERE type = (?) ORDER BY date DESC", (type,))
    result = sql.fetchmany(num)
    db.close()
    return(result)

# Выборка по видео на канале
def youtube_video_search_url(url):
    db,sql = connect()
    sql.execute("SELECT * FROM youtube_video WHERE url = (?) ", (url,))
    result = sql.fetchall()
    db.close()
    return(result)


# Локация
def check_location(id):
    db,sql = connect()
    sql.execute("SELECT * FROM subscribers WHERE id = (?) AND geonameid != (?) ", (id,'None',))
    data_list = sql.fetchone()
    # if sql.fetchone() is None:
    #     data_list = sql.fetchone()
    #     print (data_list)
    # else:
    #     data_list = sql.fetchone()
    # print (data_list)
    db.close()
    return(data_list)         


# Управление админами
def admins(id, role, memo):
    db,sql = connect()
    sql.execute("""CREATE TABLE IF NOT EXISTS admins (
        id INT PRIMARY KEY,
        role TEXT,
        memo TEXT
    ) """)
    # sql.execute("SELECT id FROM admins WHERE id = (?)", (id, ))
    # if sql.fetchone() is None:
    sql.execute("INSERT OR REPLACE INTO admins VALUES (?, ?, ?)", (id, role, memo, ))
    db.commit()
    db.close()
    return()    

def adm_list():
    db,sql = connect()
    sql.execute('SELECT * FROM admins')
    result = sql.fetchall()
    db.close()
    return(result)     

def adm_del(id):
    db,sql = connect()
    sql.execute('DELETE FROM admins WHERE id = (?)', (id,))
    db.commit()
    db.close()


# Дроп таблицы в бд
def drop_table():
    db,sql = connect()
    sql.execute('DROP TABLE ******')
    db.close()
   