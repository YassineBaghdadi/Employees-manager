import webbrowser
#test changing
import pymysql, sys, os, selenium
import requests
from firebase import firebase
import datetime

from PyQt5 import uic, QtCore, QtWidgets, QtGui

# try:
#     request = requests.get(url, timeout=timeout)
#     print("Connected to the Internet")
#
#
# except (requests.ConnectionError, requests.Timeout) as e:
#

# print('from firebase',ADMIN_ALLOWED)
CURRENT_USER = 'Anonymous'

#todo create the tables if not exists

HOST = '192.168.1.110'
SERVER_USERNAME = 'hadef'
SERVER_PASSWORD = 'p@$$w0rd'
DB = 'HadefGaz'

def db_connect():
    return pymysql.connect(host=HOST, user=SERVER_USERNAME, password=SERVER_PASSWORD, database=DB)


class PripareDB:
    def __init__(self):
        print('preparing the DB')
        try:
            con = pymysql.connect(host=HOST, user=SERVER_USERNAME, password=SERVER_PASSWORD)

            if con:
                print('connected ...')
            else:
                print('connecting failed')
                # exit()

            curs = con.cursor()

            curs.execute(f'CREATE DATABASE IF NOT EXISTS {DB};')

            # curs.execute('use HadefGaz;')

            curs.execute(f'''CREATE TABLE IF NOT EXISTS {DB}.users (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        F_name VARCHAR(20), 
                        L_name VARCHAR(20), 
                        username VARCHAR(20), 
                        passwrd VARCHAR(20)) ENGINE = INNODB;''')

            curs.execute(f'''CREATE TABLE IF NOT EXISTS {DB}.agents(
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        F_name VARCHAR(50), 
                        L_name VARCHAR(50), 
                        BD VARCHAR(50), 
                        CIN VARCHAR(50), 
                        CNSS INT, 
                        company VARCHAR(50), 
                        role_ VARCHAR(50), 
                        status VARCHAR(50), 
                        salary INT, 
                        TEL VARCHAR(50), 
                        address VARCHAR(50), 
                        img LONGBLOB, 
                        start_date VARCHAR(50), 
                        end_date VARCHAR(50)) ENGINE = INNODB;''')

            curs.execute(f'''CREATE TABLE IF NOT EXISTS {DB}.history (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        user INT, 
                        pc VARCHAR(50), 
                        opr VARCHAR(50), 
                        agent INT,
                        FOREIGN KEY (user) REFERENCES {DB}.users(id),
                        FOREIGN KEY (agent) REFERENCES {DB}.agents(id)) ENGINE = INNODB
                        ;''')

            curs.execute(f'''CREATE TABLE IF NOT EXISTS {DB}.abss (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        agent INT, 
                        abss_date VARCHAR(50),
                        FOREIGN KEY (agent) REFERENCES {DB}.agents(id)) ENGINE = INNODB;''')

            con.commit()
            con.close()
            self.login = Login()
            self.login.show()
        except (pymysql.err.OperationalError, OSError) as e:
            print(f'cant connect to the server {e}')
            self.err = Err(e)
            self.err.show()


class Err(QtWidgets.QWidget):
    def __init__(self, err=None):
        super(Err, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'err.ui'), self)
        self.move(300, 200)

        self.err_icon.setPixmap(QtGui.QPixmap('src/img/err.png'))
        self.err_icon.setScaledContents(True)
        self.err_txt = '404'
        if not err:
            self.err_txt = 'الخطلأ غير معروف'

        self.err_txt = str(err)
        self.err_msg.setText(self.err_txt)
        self.err_title.installEventFilter(self)

    def eventFilter(self, o, e):
        if e.type() == QtCore.QEvent.MouseButtonPress:
            if o is self.err_title:
                webbrowser.open('https://yassinebaghdadi.github.io/')

        return super(Err, self).eventFilter(o, e)



# class Index(QtWidgets.QWidget):
#     def __init__(self):
#         super(Index, self).__init__()
#         uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'index.ui'), self)
#         self.setGeometry(200, 200, 717, 398)
#         self.change_widget(Main())
#         print('app starting ...')
#
#
#     def change_widget(self, widget):
#         for i in reversed(range(self.index_content.count())):
#             self.index_content.itemAt(i).widget().setParent(None)
#         self.index_content.addWidget(widget)


class Login(QtWidgets.QWidget):
    def __init__(self):
        super(Login, self).__init__(None)
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'login.ui'), self)

        if not ADMIN_ALLOWED:
            self.err = Err('SYSTEM DOWN CALL DEVLOPER ')
            self.err.show()
            self.close()
        else:
            print('ADMIN ALLOWED')

        self.move(300, 200)
        self.enter.setFocus(True)

        self.enter.clicked.connect(self.login)
        



    def login(self):
        user = ''
    
        
        try:
            print('opening main page ...')
            con = db_connect()
            curs = con.cursor()
            curs.execute(f'SELECT F_name, L_name FROM users WHERE username like "{self.username.text()}" and passwrd like "{self.passwrd.text()}";')
            user = curs.fetchone()
            print(f"the current users is : {user}")
        except Exception as e:
            self.err = Err(err=e)
            self.close()
            self.err.show()

        if user:
            global CURRENT_USER
            CURRENT_USER = f'{user[0]} {user[1]}'
            self.main = Main()
            self.close()
            self.main.show()
        else:
            self.err = Err(err='المعلومات غير صحيحة')
            self.err.show()

        


class Main(QtWidgets.QFrame):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'), self)
        self.move(300, 200)
        self.history_icon.setPixmap(QtGui.QPixmap('src/img/history.png'))
        self.omal_icon.setPixmap(QtGui.QPixmap('src/img/empl.png'))
        self.history_icon.setScaledContents(True)
        self.omal_icon.setScaledContents(True)
        self.omal_btn.installEventFilter(self)
        self.history_btn.installEventFilter(self)
        print(f'Current User : {CURRENT_USER}')

    def eventFilter(self, o, e) -> bool:
        if (e.type() == QtCore.QEvent.MouseButtonPress):
            if o is self.omal_btn :
                print('opening omal ...')
                self.omal = Omal()
                self.close()
                self.omal.show()

            if o is self.history_btn:
                print('opening history ...')
                self.history = History()
                self.close()
                self.history.show()


        #
        # if e.type() == QtCore.QEvent.HoverEnter:
        #     if o == self.omal_btn :
        #         self.omal_btn.setStyleSheet('border: 5px solid blue;')
        #     if o == self.history_btn :
        #         self.history_btn.setStyleSheet('border: 1px solid blue;')


        if e.type() == QtCore.QEvent.HoverEnter:
            if o == self.omal_btn :
                print('omal hover in successfully')
                self.hover_in(self.omal_btn)
            if o == self.history_btn :
                self.hover_in(self.history_btn)




        return super(Main, self).eventFilter(o, e)

    def hover_in(self, o):
        o.setStyleSheet('border: 5px solid blue;')

    def hover_out(self, o):
        o.setStyleSheet('border: 5px solid blue;')




class Omal(QtWidgets.QWidget):
    def __init__(self):
        super(Omal, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'omal.ui'), self)
        self.move(300, 200)
        self.check_ico.setPixmap(QtGui.QPixmap('src/img/ghiyab.png'))
        self.check_ico.setScaledContents(True)
        self.add_ico.setPixmap(QtGui.QPixmap('src/img/add.png'))
        self.add_ico.setScaledContents(True)
        self.pay_ico.setPixmap(QtGui.QPixmap('src/img/pay.png'))
        self.pay_ico.setScaledContents(True)
        self.list_ico.setPixmap(QtGui.QPixmap('src/img/list.png'))
        self.list_ico.setScaledContents(True)
        self.check.installEventFilter(self)
        self.add.installEventFilter(self)
        self.pay.installEventFilter(self)
        self.empl_list.installEventFilter(self)
        self.back_btn.clicked.connect(self.back)

    def back(self):
        self.main = Main()
        self.close()
        self.main.show()

    def eventFilter(self, o, e) -> bool:
        if e.type() == QtCore.QEvent.MouseButtonPress:
            if o is self.add:
                print('opening history ...')
                self.add = Add()
                self.close()
                self.add.show()
            if o is self.empl_list:
                print('opening empl list ...')
                self.emlL =Omal_list()
                self.close()
                self.emlL.show()

            if o is self.pay:
                print('opening Paying page ...')
                self.pay_ = Pay()
                self.close()
                self.pay_.show()

            if o is self.check:
                print('opening Check in page ...')
                self.checkin = Checkin()
                self.close()
                self.checkin.show()

        if e.type() == QtCore.QEvent.HoverEnter:
            if o == self.check:
                self.check.setStyleSheet('border: 1px solid blue;')
            if o == self.pay:
                self.pay.setStyleSheet('border: 1px solid blue;')
            if o == self.empl_list:
                self.empl_list.setStyleSheet('border: 1px solid blue;')
            if o == self.add:
                self.add.setStyleSheet('border: 1px solid blue;')

        return super(Omal, self).eventFilter(o, e)


class History(QtWidgets.QWidget):
    def __init__(self, h=True):
        super(History, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'history.ui'), self)
        self.move(300, 200)
        self.h = h
        self.back_btn.clicked.connect(self.back)
        self.title = ''
        if not h:#todo for change the title if not history window
            self.title = ''

    def back(self):
        if self.h:
            self.main = Main()
        else:
            self.main = Omal()
        self.close()
        self.main.show()

class Add(QtWidgets.QWidget):
    def __init__(self):
        super(Add, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'add.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)
        self.start_date.setDate(QtCore.QDate.currentDate())
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.companies = ['هادف غاز', 'صافكام', 'سونعيمي', 'المقهى', 'هيمكة', 'أخرى']
        self.roles = ["سائق", "مساعد", "الإدارة", "أخرى"]
        self.cnss.setValidator(QtGui.QIntValidator())
        self.salary.setValidator(QtGui.QIntValidator())
        self.company.addItems(self.companies)
        self.role.addItems(self.roles)
        #todo here stopped


    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


    def save(self):
        print(str(self.BD.date().toPyDate()))
        print(str(self.company.currentText()))
        print(str(self.role.currentText()))
        if not self.F_name.text() or not self.L_name.text() or int(str(datetime.date.today().strftime("%Y-%m-%d")).split("-")[0]) - int(str(self.BD.date().toPyDate()).split("-")[0]) < 14 or self.CIN.text() == "" or self.salary.text() == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "معلومات غير مقبولة")
            return
        try:
            con = db_connect()
            curs = con.cursor()
            #curs.execute("set names utf8;")
            curs.execute(f'''
                    insert into agents (F_name, L_name, BD, CIN, CNSS, company, role_, status, salary, TEL, address, img, start_date) values(
                    "{self.F_name.text()}",
                    "{self.L_name.text()}",
                    "{str(self.BD.date().toPyDate())}",
                    "{self.CIN.text()}",
                     {self.cnss.text()},
                    "{str(self.company.currentText())}",
                    "{str(self.role.currentText())}",
                    "{1}",
                    "{self.salary.text()}",
                    "{self.tel.text()}",
                    "{self.address.text()}",
                    " ",
                    "{str(self.start_date.date().toPyDate())}"
                )''')#todo fix the image storage and start date validator for the db
            con.commit()
            con.close()
            self.cancel()
        except (pymysql.err.OperationalError, OSError, pymysql.err.DataError, pymysql.err.ProgrammingError) as e:
            print(f'cant connect to the server {e}')
            self.err = Err(e)
            self.err.show()
            self.close()

    def cancel(self):
        self.F_name.setText('')
        self.L_name.setText('')
        self.CIN.setText('')
        self.BD.setDate(QtCore.QDate(2000, 1, 1))
        self.address.setText('')
        self.tel.setText('')
        self.salary.setText('')
        self.cnss.setText('')
        self.company.setCurrentIndex(0)
        self.role.setCurrentIndex(0)
        self.start_date.setDate(QtCore.QDate.currentDate())


class Pay(QtWidgets.QWidget):
    def __init__(self):
        super(Pay, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'pay.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)


    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()

class Omal_list(QtWidgets.QWidget):
    def __init__(self):
        super(Omal_list, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'omal_list.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)
        comps = [ 'هادف غاز', 'صافكام', 'سونعيمي', 'المقهى', 'هيمكة', 'أخرى']
        self.copanies_combo.addItems(comps)
        self.copanies_combo.setCurrentIndex(0)
        self.copanies_combo.currentTextChanged.connect(self.fill)
        self.search.textChanged.connect(self.fill)
        self.fill()


        """
            self.home_table.viewport().installEventFilter(self)

            def eventFilter(self, source, event):
                if (event.type() == QtCore.QEvent.MouseButtonDblClick and
                        source is self.home_table.viewport()):
                    item = self.home_table.itemAt(event.pos())
                    if item is not None:
                        print('dblclick:', item.row(), item.column())
                        if self.comboBox.currentIndex() == 1:
                            row = [self.home_table.item(item.row(), c).text() for c in range(self.home_table.columnCount())]
                            print(row)
                            self.prod_inf = Product_info([self.home_table.item(item.row(), 0).text(), item.column()])
                            self.prod_inf.show()
                        elif self.comboBox.currentIndex() == 0:
                            self.search_txt.setText(self.home_table.item(item.row(), item.column()).text())
                return super(Home, self).eventFilter(source, event)
            """


    def fill(self):
        print(self.copanies_combo.currentText())
        [self.omal_table.removeRow(0) for _ in range(self.omal_table.rowCount())]
        head = ["الإسم", "النسب", "البطاقة الوطنية", "المهمة", "الشركة", "الهاتف", "العنوان", "تاريخ الإلتحاق"]

        # self.omal_table.horizontalHeader().setSectionResizeMode(head.index(self.head[-1]), QtWidgets.QHeaderView.Stretch)
        # for i in range(len(head)):
        #     self.omal_table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        con = db_connect()
        curs = con.cursor()
        #qury = ""

        if self.search.text():
            qury = f"""SELECT F_name, L_name, CIN, role_, company, TEL, address, start_date FROM agents WHERE ( status like '1' and company like '%{self.copanies_combo.currentText()}%') and (F_name LIKE '%{self.search.text()}%' or L_name LIKE '%{self.search.text()}%' or CIN LIKE '%{self.search.text()}%'); """


        else:
            qury = f"SELECT F_name, L_name, CIN, role_, company, TEL, address, start_date FROM agents WHERE status like '1' and company like '{self.copanies_combo.currentText()}';"

        curs.execute(qury)

        data = curs.fetchall()
        print(data)
        if not data :
            return
        self.omal_table.setColumnCount(len(data[0]))
        self.omal_table.setHorizontalHeaderLabels(head)
        # self.omal_table.horizontalHeader().setSectionResizeMode(head.index(self.head[-1]), QtWidgets.QHeaderView.Stretch)
        # self.omal_table.resizeColumnsToContents()
        # self.omal_table.setRowCount(len(data))
        for i in range(len(head)):
            self.omal_table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        for r in range(len(data)):
            self.omal_table.insertRow(0)
            for c in range(len(data[r])):
                self.omal_table.setItem(0, c, QtWidgets.QTableWidgetItem(data[r][c]))

        con.close()

    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


class Checkin(QtWidgets.QWidget):
    def __init__(self):
        super(Checkin, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'checkin.ui'), self)

        self.move(300, 200)
        self.cancel.clicked.connect(self.back)

    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


class Logs():
    def __init__(self, user, operation_id ):
        pass




if __name__ == '__main__':
    # print(f'from firebase : {ADMIN_ALLOWED}')
    # print(f'Current User before : {CURRENT_USER}')
    app = QtWidgets.QApplication(sys.argv)

    ADMIN_ALLOWED = 1
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'i.json')):
        print('the file is here ')
        try:
            print('trying to connect to internet ...')
            r = requests.get('http://172.217.168.164', timeout=2)
            print('there is an internet')
            ADMIN_ALLOWED = int(firebase.FirebaseApplication('https://p-e-i-5ea0c.firebaseio.com/', None).get('HadefGaz/empoyee_salary_manager', ''))

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print(f'no internet : {e}')

        if not ADMIN_ALLOWED:
                print('the admin has stopped the app remotly')
                os.remove(os.path.join(os.path.dirname(__file__), 'i.json'))
                err = Err('SYSTEM DOWN CALL THE DEVELOPER ')
                err.show()
        else:

                print('go to priparing db class ')
                pr = PripareDB()
    else:
        print('no file found')
        err = Err('SYSTEM DOWN CALL THE DEVELOPER ')
        err.show()


    # err = Err(err='test')
    # err.show()
    app.exec_()
