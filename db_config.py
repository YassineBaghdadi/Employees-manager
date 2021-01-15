import pymysql
con = ''
try:
    con = pymysql.connect('192.168.1.110', 'hadef', 'p@$$w0rd')
except pymysql.err.OperationalError as e:
    print(e)


if con:
    print('connected ...')
else:
    print('connecting failed')
    exit()

curs = con.cursor()

curs.execute('CREATE DATABASE IF NOT EXISTS HadefGaz;')


# curs.execute('use HadefGaz;')


curs.execute('''CREATE TABLE IF NOT EXISTS HadefGaz.users (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            F_name VARCHAR(20), 
            L_name VARCHAR(20), 
            username VARCHAR(20), 
            passwrd VARCHAR(20));''')


curs.execute('''CREATE TABLE IF NOT EXISTS HadefGaz.agents(
            id INT AUTO_INCREMENT PRIMARY KEY, 
            F_name VARCHAR(20), 
            L_name VARCHAR(20), 
            BD VARCHAR(50), 
            CIN VARCHAR(20),
            CNSS INT, 
            company VARCHAR(20), 
            role VARCHAR(20), 
            status VARCHAR(20), 
            salary INT, 
            TEL VARCHAR(20), 
            address VARCHAR(50), 
            img LONGBLOB, 
            start_date VARCHAR(30), 
            end_date VARCHAR(30));''')


curs.execute('''CREATE TABLE IF NOT EXISTS HadefGaz.history (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            user INT, 
            pc VARCHAR(20), 
            opr VARCHAR(20), 
            agent INT,
            FOREIGN KEY (user) REFERENCES HadefGaz.users(id),
            FOREIGN KEY (agent) REFERENCES HadefGaz.agents(id))
            ;''')


curs.execute('''CREATE TABLE IF NOT EXISTS HadefGaz.abss (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            agent INT, 
            abss_date VARCHAR(20),
            FOREIGN KEY (agent) REFERENCES HadefGaz.agents(id));''')




con.commit()
