import webbrowser
#test changing
import pymysql, sys, os, selenium
import requests
# from firebase import firebase
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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

CURRENT_USER = 'Anonymous'
ADMIN_ALLOWED = 1
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


        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'i.json')):
            print('the file is here ')
            try:
                # try:
                #     print('trying to connect to internet ...')
                #     r = requests.get('http://172.217.168.164', timeout=2)
                #     print('there is an internet')
                # except Exception as e:
                #     print(f'{e}')
                global ADMIN_ALLOWED
                # try:
                #
                #     ADMIN_ALLOWED = int(firebase.FirebaseApplication('https://p-e-i-5ea0c.firebaseio.com/', None).get(
                #         'HadefGaz/empoyee_salary_manager', ''))
                # except:
                #     pass
                if not ADMIN_ALLOWED:
                    print('the admin has stopped the app remotly')
                    os.remove(os.path.join(os.path.dirname(__file__), 'i.json'))
                    err = Err('SYSTEM DOWN CALL THE DEVELOPER ')
                    err.show()
                    return


                try:
                    con = pymysql.connect(host=HOST, user=SERVER_USERNAME, password=SERVER_PASSWORD)

                    if con:
                        print('connected ...')
                    else:
                        print('connecting failed')
                        err = Err('SYSTEM DOWN CALL THE DEVELOPER CQNT CONNECT TO DB')
                        err.show()
                        return

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
                                CNSS VARCHAR(50), 
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
                                op_date VARCHAR(50),
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


                    curs.execute(f'''CREATE TABLE IF NOT EXISTS {DB}.paids (
                                id INT AUTO_INCREMENT PRIMARY KEY, 
                                agent INT,
                                amount VARCHAR(50),
                                paid_date VARCHAR(50),
                                FOREIGN KEY (agent) REFERENCES {DB}.agents(id)) ENGINE = INNODB;''')

                    con.commit()
                    con.close()
                    self.login = Login()
                    self.login.show()
                except (pymysql.err.OperationalError, OSError) as e:
                    print(f'cant connect to the server {e}')
                    self.err = Err(e)
                    self.err.show()

            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                print(f'no internet : {e}')



        else:
            print('no file found')
            err = Err('SYSTEM DOWN CALL THE DEVELOPER ')
            err.show()

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

        # if not ADMIN_ALLOWED:
        #     self.err = Err('SYSTEM DOWN CALL DEVLOPER ')
        #     self.err.show()
        #     self.close()
        # else:
        #     print('ADMIN ALLOWED')

        self.move(300, 200)
        self.enter.setFocus(True)

        self.enter.clicked.connect(self.login)

        # self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)


    def login(self):
        try:
            print('opening main page ...')
            con = db_connect()
            curs = con.cursor()
            curs.execute(f'SELECT F_name, L_name FROM users WHERE username like "{self.username.text()}" and passwrd like "{self.passwrd.text()}";')
            user = curs.fetchone()
            print(f"the current user is : {user}")
            if user:
                global CURRENT_USER
                CURRENT_USER = f'{user[0]} {user[1]}'
                self.main_ = Main()
                self.main_.show()
                self.close()

            else:
                self.err = Err(err='المعلومات غير صحيحة')
                self.err.show()
            con.close()
        except Exception as e:
            self.err = Err(err=e)
            self.close()
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

        #
        # if e.type() == QtCore.QEvent.HoverEnter:
        #     if o == self.omal_btn :
        #         print('omal hover in successfully')
        #         self.hover_in(self.omal_btn)
        #     if o == self.history_btn :
        #         self.hover_in(self.history_btn)




        return super(Main, self).eventFilter(o, e)


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
    def __init__(self, id = None):
        super(Add, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'add.ui'), self)
        self.move(300, 200)
        self.idd = id
        self.companies = ['هادف غاز', 'صافكام', 'سونعيمي', 'المقهى', 'هيمكة', 'أخرى']
        self.roles = ["سائق", "مساعد", "الإدارة", "أخرى"]

        self.end_date.setFixedWidth(0)
        self.back_btn.clicked.connect(self.back)
        self.start_date.setDate(QtCore.QDate.currentDate())
        self.end_date.setDate(QtCore.QDate.currentDate())
        self.cancel_btn.clicked.connect(self.cancel)
        self.cnss.setValidator(QtGui.QIntValidator())
        self.salary.setValidator(QtGui.QIntValidator())
        self.company.addItems(self.companies)
        self.role.addItems(self.roles)
        self.status.stateChanged.connect(self.status_changed)
        if self.idd:
            self.fill(id)
            self.save_btn.clicked.connect(self.edit)
            self.cancel_btn.setEnabled(False)
        else:
            self.save_btn.clicked.connect(self.save)


    def status_changed(self):
        if self.status.isChecked():
            self.end_date.setEnabled(False)
            self.end_date.setFixedWidth(0)

        else:
            self.end_date.setEnabled(True)
            self.end_date.setFixedWidth(182)

    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


    def fill(self, id):
        try:
            con = db_connect()
            print('connected')
            curs = con.cursor()
            print(id)
            try:
                if os.path.isfile(f'src/img/emps/{id}.png'):
                    self.profile_img.setPixmap(QtGui.QPixmap(f'src/img/emps/{id}.png'))
                    self.profile_img.setScaledContents(True)
                else:
                    self.profile_img.setPixmap(QtGui.QPixmap(f'src/img/no-image.png'))
                    self.profile_img.setScaledContents(True)

            except:pass

            curs.execute(f'''SELECT * FROM agents WHERE id = {id} ;''')
            d = [i for i in curs.fetchall()[0]]
            self.F_name.setText(str(d[1]))
            self.L_name.setText(str(d[2]))
            self.CIN.setText(str(d[4]))
            self.BD.setDate(QtCore.QDate(int(d[3].split('-')[0]), int(d[3].split('-')[1]), int(d[3].split('-')[2])))
            print(f'start date : {d[13]}')
            self.start_date.setDate(QtCore.QDate(int(d[13].split('-')[0]), int(d[13].split('-')[1]), int(d[13].split('-')[2])))
            self.address.setText(d[11])
            self.tel.setText(d[10])
            self.salary.setText(str(d[9]))
            self.cnss.setText(d[5])

            print('company ', self.companies.index(d[6]))
            index = self.company.findText(d[6], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.company.setCurrentIndex(index)


            index = self.role.findText(d[7], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.role.setCurrentIndex(index)

            if d[8] == 'نشط' :
                self.status.setChecked(True)
            else :
                self.status.setChecked(False)
                self.end_date.setDate(QtCore.QDate(int(d[14].split('-')[0]), int(d[14].split('-')[1]), int(d[14].split('-')[2])))

            print(d)

        except Exception as e:
            print(f'cant connect to the server {e}')
            self.close()
            self.err = Err(e)
            self.err.show()



    def edit(self):
        if not self.F_name.text() or not self.L_name.text() or int(str(datetime.date.today().strftime("%Y-%m-%d")).split("-")[0]) - int(str(self.BD.date().toPyDate()).split("-")[0]) < 14 or self.CIN.text() == "" or self.salary.text() == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "معلومات غير مقبولة")
            return



        try:
            con = db_connect()
            print('connected')
            curs = con.cursor()
            # curs.execute(f'''select id from agents where CIN like "{self.CIN.text()}" ;''')
            # if curs.fetchone():
            #     QtWidgets.QMessageBox.about(self, "ERROR", "رقم البطاقة الوطنية موجود في معلومات شخص اخر")
            #     return
            # curs.execute("set names utf8;")
            curs.execute(f'''
                        update agents set
                         F_name = "{self.F_name.text()}",
                         L_name = "{self.L_name.text()}",
                         BD = "{str(self.BD.date().toPyDate())}",
                         CIN = "{self.CIN.text()}",
                         CNSS = "{self.cnss.text()}",
                         company = "{str(self.company.currentText())}",
                         role_ = "{str(self.role.currentText())}",
                         status = "{'نشط' if self.status.isChecked() else 'متوقف'}",
                         salary = {int(self.salary.text())},
                         TEL = "{self.tel.text()}",
                         address = "{self.address.text()}",
                         img = " ",
                         start_date = "{str(self.start_date.date().toPyDate())}" ,
                         end_date = "{str(self.end_date.date().toPyDate()) if not self.status.isChecked() else ''}"
                         where id = {self.idd}
                         
                    ''')

            con.commit()
            con.close()
            self.cancel()
        except (pymysql.err.OperationalError, OSError, pymysql.err.DataError, pymysql.err.ProgrammingError) as e:
            print(f'cant connect to the server {e}')
            self.err = Err(e)
            self.err.show()
            self.close()


    def save(self):
        print(str(self.BD.date().toPyDate()))
        print(str(self.company.currentText()))
        print(str(self.role.currentText()))
        if not self.F_name.text() or not self.L_name.text() or int(str(datetime.date.today().strftime("%Y-%m-%d")).split("-")[0]) - int(str(self.BD.date().toPyDate()).split("-")[0]) < 14 or self.CIN.text() == "" or self.salary.text() == "":
            QtWidgets.QMessageBox.about(self, "ERROR", "معلومات غير مقبولة")
            return

        try:
            con = db_connect()
            print('connected')
            curs = con.cursor()
            curs.execute(f'''select id from agents where CIN like "{self.CIN.text()}" ;''')
            if curs.fetchone():
                QtWidgets.QMessageBox.about(self, "ERROR", "هذا الشخص موجود بالفعل")
                return
            # curs.execute("set names utf8;")
            curs.execute(f'''
                    insert into agents (F_name, L_name, BD, CIN, CNSS, company, role_, status, salary, TEL, address, img, start_date, end_date) values(
                    "{self.F_name.text()}",
                    "{self.L_name.text()}",
                    "{str(self.BD.date().toPyDate())}",
                    "{self.CIN.text()}",
                    "{self.cnss.text()}",
                    "{str(self.company.currentText())}",
                    "{str(self.role.currentText())}",
                    "{'نشط' if self.status.isChecked() else 'متوقف'}",
                    {int(self.salary.text())},
                    "{self.tel.text()}",
                    "{self.address.text()}",
                    " ",
                    "{str(self.start_date.date().toPyDate())}",
                    "{str(self.end_date.date().toPyDate()) if not self.status.isChecked() else ''}"
                );''')#todo fix the image storage and start date validator for the db
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
    def __init__(self, id_ = None):
        super(Pay, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'pay.ui'), self)
        self.move(300, 200)

        self.back_btn.clicked.connect(self.back)
        self.con = db_connect()
        self.curs = self.con.cursor()
        self.curs.execute("SELECT F_name, L_name, id, company FROM agents ORDER BY F_name ASC ;")
        agents = [f"{i[0]} {i[1]} -{i[2]}- {i[3]}" for i in self.curs.fetchall()]
        agents.insert(0, '')
        self.omal_combo.addItems(agents)
        self.omal_combo.currentTextChanged.connect(self.fill)
        self.pay_btn.clicked.connect(self.pay)
        self.pay_date.setDate(QtCore.QDate.currentDate())
        self.to_pay.textChanged.connect(self.virf_amount)
        self.to_pay.setEnabled(False)

        if id_:
            for i in range(1, len(agents)):
                if int(str(self.omal_combo.itemText(i)).split('-')[1]) == id_:
                    self.omal_combo.setCurrentIndex(i)
                    break



    def virf_amount(self):
        try:
            if float(self.to_pay.text()) > float(str(self.rest.text()).strip().replace(' ', '').replace('dh', '')):
                self.pay_btn.setEnabled(False)
            else:
                self.pay_btn.setEnabled(True)
        except:
            self.to_pay.clear()

    def pay(self):
        if self.omal_combo.currentIndex() == 0:
            QtWidgets.QMessageBox.about(self, "ERROR", "إختر العامل أولا")
            return

        if not self.to_pay.text() :
            QtWidgets.QMessageBox.about(self, "ERROR", "أدخل المبلغ أولا")
            return



        self.curs.execute(f'''insert into paids (agent, amount, paid_date) value ({int(self.omal_combo.currentText().split('-')[1])}, "{self.to_pay.text()}", "{str(self.pay_date.date().toPyDate())}")''')
        self.con.commit()
        self.to_pay.setText('')
        self.omal_combo.setCurrentIndex(0)
        self.pay_date.setDate(QtCore.QDate.currentDate())

    def fill(self):
        self.to_pay.clear()
        if not self.omal_combo.currentText():
            self.salary.setText('0 DH')
            self.working_period.setText('0')
            self.start_date.setText('0')
            self.abssences.setText('0')
            self.amount_paid.setText('0')
            self.rest.setText('0')
            self.to_pay.setEnabled(False)
            return

        self.to_pay.setEnabled(True)


        self.curs.execute(f'''SELECT salary, start_date FROM agents WHERE id = {int(self.omal_combo.currentText().split('-')[1])}''')
        salary, start_date = self.curs.fetchone()
        # self.curs.execute(f'''SELECT count(id), amount from paids where agent = {int(self.omal_combo.currentText().split('-')[1])} and paid_date like "{datetime.date.today().strftime("%Y-%m")}%"''') for this month only
        self.curs.execute(f'''SELECT amount from paids where agent = {int(self.omal_combo.currentText().split('-')[1])}''')
        dt = [float(i[0]) for i in self.curs.fetchall() if i]
        print(dt)
        amount_paids = sum(dt) if dt else 0
        print(f'amount paids ({type(amount_paids)}) = {amount_paids}')
        # self.curs.execute(f'''select count(id) from abss where agent = {int(self.omal_combo.currentText().split('-')[1])} and abss_date like "{datetime.date.today().strftime("%Y-%m")}%"''') for this month only
        self.curs.execute(f'''select count(id) from abss where agent = {int(self.omal_combo.currentText().split('-')[1])}''')
        mounths_abbs_days = self.curs.fetchone()
        print(mounths_abbs_days)

        self.salary.setText(f'{str(salary)} DH')
        self.start_date.setText(start_date)
        self.amount_paid.setText(str(amount_paids) if amount_paids else '0')
        day = salary / 30

        self.curs.execute(f'''select end_date from agents where id = {int(self.omal_combo.currentText().split('-')[1])}''')
        e_date = self.curs.fetchone()[0]
        print(e_date)
        today = str(datetime.date.today().strftime("%Y-%m-%d"))
        print('###################')

        if int(start_date.split('-')[0]) < 2021 :
            start_date = '2021-01-01'

        if e_date:
            days_of_work = datetime.date(int(e_date.split('-')[0]),int(e_date.split('-')[1]),int(e_date.split('-')[2]) )- datetime.date(int(start_date.split('-')[0]),int(start_date.split('-')[1]),int(start_date.split('-')[2]) )
        else:
            days_of_work = datetime.date(int(today.split('-')[0]),int(today.split('-')[1]),int(today.split('-')[2]) ) - datetime.date(int(start_date.split('-')[0]),int(start_date.split('-')[1]),int(start_date.split('-')[2]) )
        print(days_of_work.days)
        works_peried_days = days_of_work.days
        if int(datetime.datetime.now().strftime("%d/%m/%Y %H:%M").split(':')[-1]) > 12:
            works_peried_days += 1


        # self.rest.setText(str(round((salary-(amount_paids+(day * int(mounths_abbs_days[0])))), 2))) for this month only
        self.rest.setText(str(round((((works_peried_days - mounths_abbs_days[0]) * day)-(amount_paids)), 2)))
        if not float(round((salary-(amount_paids+(day * int(mounths_abbs_days[0])))), 2)):
            self.pay_btn.setEnabled(False)
        else:
            self.pay_btn.setEnabled(True)


    def back(self):
        self.con.close()
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
        self.add.clicked.connect(self.add_emp)
        self.omal_table.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonDblClick and source is self.omal_table.viewport()):
            items = self.omal_table.itemAt(event.pos())
            if items is not None:
                print('dblclick:', items.row(), items.column())
                print(self.omal_table.item(items.row(), items.column()).text())
                #table double click

                msgbox = QtWidgets.QMessageBox()
                # msgbox.setText('إختيار')
                msgbox.setWindowModality(QtCore.Qt.NonModal)
                msgbox.setWindowTitle('yassine')
                edite = msgbox.addButton('تعديل', msgbox.ActionRole)
                abss = msgbox.addButton('غياب', msgbox.ActionRole)
                pay = msgbox.addButton('دفع', msgbox.ActionRole)
                print(f'the Output is : {int(self.omal_table.item(items.row(), 0).text())}')

                def make_abss():
                    self.abss = Checkin(id=int(self.omal_table.item(items.row(), 0).text()))
                    self.close()
                    self.abss.show()

                def make_edite():
                    self.modify = Add(self.omal_table.item(items.row(), 0).text())
                    self.modify.show()
                    self.close()
                def make_pay():
                    self.pay = Pay(id_=int(self.omal_table.item(items.row(), 0).text()))
                    self.close()
                    self.pay.show()


                abss.clicked.connect(make_abss)
                pay.clicked.connect(make_pay)
                edite.clicked.connect(make_edite)

                msgbox.exec_()
        return super(Omal_list, self).eventFilter(source, event)




    def add_emp(self):
        self.addd = Add()
        self.close()
        self.addd.show()


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
        head = ["الإسم", "النسب", "البطاقة الوطنية", "المهمة", "الشركة", "الهاتف", "العنوان", "تاريخ الإلتحاق", "الوضعية"]
        head.insert(0, 'الرقم التسلسلي')
        # self.omal_table.horizontalHeader().setSectionResizeMode(head.index(self.head[-1]), QtWidgets.QHeaderView.Stretch)
        # for i in range(len(head)):
        #     self.omal_table.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        con = db_connect()
        curs = con.cursor()
        #qury = ""

        if self.search.text():
            qury = f"""SELECT id, F_name, L_name, CIN, role_, company, TEL, address, start_date, status FROM agents WHERE (company like '%{self.copanies_combo.currentText()}%') and (F_name LIKE '%{self.search.text()}%' or L_name LIKE '%{self.search.text()}%' or CIN LIKE '%{self.search.text()}%') order by L_name DESC; """


        else:
            qury = f"SELECT id, F_name, L_name, CIN, role_, company, TEL, address, start_date, status FROM agents WHERE company like '{self.copanies_combo.currentText()}' order by L_name DESC;"

        curs.execute(qury)

        # data = curs.fetchall()
        data = [[c for c in i] for i in  curs.fetchall()]
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
                self.omal_table.setItem(0, c, QtWidgets.QTableWidgetItem(str(data[r][c])))

        con.close()

    def back(self):
        self.main = Omal()
        self.close()
        self.main.show()


class Checkin(QtWidgets.QWidget):
    def __init__(self, id = None):
        super(Checkin, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui', 'checkin.ui'), self)

        self.move(300, 200)
        self.cancel.clicked.connect(self.back)
        self.con = db_connect()
        self.curs = self.con.cursor()
        self.curs.execute("SELECT F_name, L_name, id, company FROM agents WHERE status like 'نشط'  ORDER BY F_name ASC ;")
        agents = [f"{i[0]} {i[1]} -{i[2]}- {i[3]}" for i in self.curs.fetchall()]
        agents.insert(0, '')
        print(agents)

        self.omal_combo.addItems(agents)
        self.add.clicked.connect(self.add_)
        self.abss_date.setDate(QtCore.QDate.currentDate())
        self.head = ["الإسم", "النسب", "البطاقة الوطنية", "الشركة", "الهاتف", "تاريخ الغياب"]
        # for i in range(len(self.head)):
        #     self.table_.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.omal_combo.currentTextChanged.connect(self.fill)
        self.abss_date.dateChanged.connect(self.fill)

        if id:
            for i in range(1, len(agents)):
                if int(str(self.omal_combo.itemText(i)).split('-')[1]) == id:
                    self.omal_combo.setCurrentIndex(i)
                    break

        self.fill()

    def fill(self):
        [self.table_.removeRow(0) for _ in range(self.table_.rowCount())]
        if not self.omal_combo.currentText():
            self.curs.execute(f"SELECT agents.F_name, agents.L_name, agents.CIN, agents.company, agents.TEL, abss.abss_date FROM agents INNER JOIN abss ON abss.agent = agents.id where abss.abss_date like '{str(self.abss_date.date().toPyDate())}';")
        else:
            if '-' in self.omal_combo.currentText():
                print(int(self.omal_combo.currentText().split('-')[1]))
                self.curs.execute(f"SELECT agents.F_name, agents.L_name, agents.CIN, agents.company, agents.TEL, abss.abss_date FROM agents INNER JOIN abss ON abss.agent = agents.id where abss.agent = {int(self.omal_combo.currentText().split('-')[1])};")


        data = self.curs.fetchall()
        print(data)
        if not data:
            return

        self.table_.setColumnCount(len(data[0]))
        self.table_.setHorizontalHeaderLabels(self.head)

        for r in range(len(data)):
            self.table_.insertRow(0)
            for c in range(len(data[r])):
                self.table_.horizontalHeader().setSectionResizeMode(c, QtWidgets.QHeaderView.Stretch)
                self.table_.setItem(0, c, QtWidgets.QTableWidgetItem(data[r][c]))


    def add_(self):
        today = str(datetime.date.today().strftime("%Y-%m-%d"))
        abss_date = str(self.abss_date.date().toPyDate())
        defernte = datetime.date(int(today.split('-')[0]), int(today.split('-')[1]), int(today.split('-')[2])) - datetime.date(
            int(abss_date.split('-')[0]), int(abss_date.split('-')[1]), int(abss_date.split('-')[2]))
        if defernte.days < 0:
            QtWidgets.QMessageBox.about(self, "ERROR", "تاريخ غير مقبول")
            return


        if self.omal_combo.currentIndex() == 0:
            QtWidgets.QMessageBox.about(self, "ERROR", "إختر العامل أولا")
            return


        self.curs.execute(f'''select * from abss where agent like "{str(self.omal_combo.currentText().split('-')[1])}" and abss_date like "{str(self.abss_date.date().toPyDate())}"''')
        if self.curs.fetchall():
            QtWidgets.QMessageBox.about(self, "ERROR", "العامل غائب بالفعل")
            return

        self.curs.execute(f"insert into abss(agent, abss_date) value ('{str(self.omal_combo.currentText().split('-')[1])}', '{str(self.abss_date.date().toPyDate())}')")
        self.con.commit()
        self.fill()

    def back(self):
        self.con.close()
        self.main = Omal()
        self.close()
        self.main.show()


class Logs():
    def __init__(self, user, operation_id ):
        pass



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setWindowIcon(QtGui.QIcon('src/img/logo.png'))
    start = PripareDB()
    sys.exit(app.exec_())
